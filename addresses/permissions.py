from rest_framework import permissions
from .models import Address


class AddressPermisson(permissions.BasePermission):
    def has_permission(self, request, view):
        user_id = request.user.id
        address = Address.objects.filter(user_id=user_id)

        try:
            address_id = list(address.values())[0]["id"]
        except:
            return False

        path_request = str(request.get_full_path())

        index = path_request.find(str(address_id))

        if index != -1:
            return True

