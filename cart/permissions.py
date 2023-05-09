from rest_framework import permissions
from .models import Cart, CartProducts
from rest_framework.views import View

class IsAdminOrCartOwner(permissions.BasePermission):
    def has_object_permission(self, request, view: View, obj) -> bool:
        if isinstance(obj, Cart):
            owner = obj.buyer
        elif isinstance(obj, CartProducts):
            owner = obj.cart.buyer
        else:
            return False

        return request.user.is_authenticated and (request.user.is_superuser or owner == request.user)
