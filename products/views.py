from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrAdmin, IsOwner, IsNotAdmin

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.action in ['update', 'partial_update']:
            self.permission_classes = [IsOwner]
        elif self.action == 'destroy':
            self.permission_classes = [IsOwnerOrAdmin]
        elif self.action == 'create':
            self.permission_classes = [IsNotAdmin]
        else:
            self.permission_classes = [IsAuthenticatedOrReadOnly]
        return super(ProductViewSet, self).get_permissions()
    
    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

