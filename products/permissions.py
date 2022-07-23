from rest_framework import permissions


class GetPostPermission(permissions.BasePermission):
    def has_permission(self, request, _):
        if request.method == "GET":
            return True
        return request.user.is_authenticated and request.user.is_seller


class OwnerOfTheProduct(permissions.BasePermission):
    def has_object_permission(self, request, _, validated_data):
        if request.method == "GET":
            return True
        return validated_data.seller == request.user
