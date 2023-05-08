from rest_framework import permissions
from .models import Cart
from rest_framework.views import View


class IsAdminOrCartOwner(permissions.BasePermission):
    def has_object_permission(self, request, view: View, obj: Cart) -> bool:
        if not request.user.is_superuser:
            return request.user.is_authenticated and obj.buyer == request.user

        return request.user.is_superuser
