from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrAdmin, IsOwner

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.action in ['update', 'partial_update']:
            self.permission_classes = [IsOwner]
        elif self.action == 'destroy':
            self.permission_classes = [IsOwnerOrAdmin]
        else:
            self.permission_classes = [IsAuthenticated]
        return super(ProductViewSet, self).get_permissions()

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

