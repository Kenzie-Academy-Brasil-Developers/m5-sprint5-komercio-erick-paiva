from re import I
from rest_framework.views import APIView, Request, Response, status

from users.permissions import OwnerOfTheAccount
from users.utils import CustomMixin
from .models import User
from .serializers import LoginSerializer, UserPatchSerializer, UserSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication


class UserLoginView(APIView):
    def post(self, request: Request):
        serialized = LoginSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)

        user: User = authenticate(**serialized.validated_data)

        if not user:
            return Response(
                {"error": "Email or password is incorrect"},
                status.HTTP_401_UNAUTHORIZED,
            )

        token, _ = Token.objects.get_or_create(user=user)

        return Response({"token": token.key}, status.HTTP_200_OK)


class UserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        date_joined = self.kwargs["num"]
        return self.queryset.order_by("-date_joined")[0:date_joined]


class UserDetailView(CustomMixin, RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [OwnerOfTheAccount]
    queryset = User.objects.all()
    serializer_map = {
        "PATCH": UserPatchSerializer,
    }

    def patch(self, request, *args, **kwargs):
        if not request.user.is_superuser and request.data.get("is_active") == False:
            return Response(
                {"error": "You cannot change this property"},
                status.HTTP_401_UNAUTHORIZED,
            )

        return self.partial_update(request, *args, **kwargs)
