from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from products.permissions import GetPostPermission, OwnerOfTheProduct
from products.utils import CustomMixin
from .models import Product
from .serializers import GetProductsSerializer, ProductSerializer
from rest_framework.authentication import TokenAuthentication


class ProductView(CustomMixin, ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [GetPostPermission]
    queryset = Product.objects.all()
    serializer_map = {
        "GET": GetProductsSerializer,
        "POST": ProductSerializer,
    }


class ProductDetailView(CustomMixin, RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [OwnerOfTheProduct]
    queryset = Product.objects.all()
    serializer_map = {
        "GET": GetProductsSerializer,
        "PATCH": ProductSerializer,
    }
