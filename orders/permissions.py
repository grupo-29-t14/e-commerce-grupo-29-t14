from rest_framework import permissions
from .models import Order


class UpdateOrderPermisson(permissions.BasePermission):
    def has_permission(self, request, view):

        user_id = request.user.id

        order_id = Order.objects.filter(seller_id=user_id)

        order_list = list(order_id)

        for order in order_list:
            if order.seller_id == user_id:
                return True

        if request.user.is_superuser:
            return True


class DeleteOrderPermisson(permissions.BasePermission):
    def has_permission(self, request, view):

        user_id = request.user.id

        order_id = Order.objects.filter(user_id=user_id)

        order_list = list(order_id)

        for order in order_list:
            if order.user_id == user_id:
                return True

        order_seller = Order.objects.filter(seller_id=user_id)

        order_list_seller = list(order_seller)

        for order in order_list_seller:
            if order.seller_id == user_id:
                return True

        if request.user.is_superuser:
            return True
