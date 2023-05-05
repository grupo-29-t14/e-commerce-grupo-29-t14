from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    # message = "Você não tem permissão para realizar esta operação."
    
    def has_object_permission(self, request,view, obj):
        return request.user == obj.seller or request.user.is_superuser

class IsNotAdmin(permissions.BasePermission):
    # message = "Administradores não podem vender produtos nesta plataforma."
    
    def has_permission(self, request,view):
        return not request.user.is_superuser

class IsOwner(permissions.BasePermission):
    # message = "Apenas o dono pode alterar as informações do produto."

    def has_object_permission(self, request, view, obj):
        return obj.seller == request.user
