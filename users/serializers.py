from django.forms import ValidationError
from rest_framework import serializers

from users.models import User


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(source="username")
    password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "is_seller",
            "date_joined",
            "password",
        )
        extra_kwargs = {
            "password": {"write_only": True},
            "is_active": {"write_only": True},
        }

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "is_seller",
            "date_joined",
            "is_active",
        )
