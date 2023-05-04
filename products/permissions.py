from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    message = "Você não tem permissão para realizar esta operação."
    
    def has_object_permission(self, request,view, obj):
        return request.user == obj.seller or request.user.is_superuser

from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    message = "Apenas o dono pode alterar as informações do produto."

    def has_object_permission(self, request, view, obj):
        return obj.seller == request.user
