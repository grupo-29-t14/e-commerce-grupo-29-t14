from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrAdmin, IsOwner, IsNotAdmin
from drf_spectacular.utils import extend_schema


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.action in ["update", "partial_update"]:
            self.permission_classes = [IsOwner]
        elif self.action == "destroy":
            self.permission_classes = [IsOwnerOrAdmin]
        elif self.action == "create":
            self.permission_classes = [IsNotAdmin]
        else:
            self.permission_classes = [IsAuthenticatedOrReadOnly]
        return super(ProductViewSet, self).get_permissions()

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

    @extend_schema(
        operation_id="get_all_products",
        responses={200: ProductSerializer(many=True)},
        description="Get all products",
        summary="Get all products",
        tags=["Products"],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        operation_id="get_product_by_id",
        responses={200: ProductSerializer(many=False)},
        description="Get product by id",
        summary="Get product by id",
        tags=["Products"],
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        operation_id="create_product",
        request=ProductSerializer(),
        responses={201: ProductSerializer(many=False)},
        description="Create product",
        summary="Create product",
        tags=["Products"],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        operation_id="update_product",
        request=ProductSerializer(),
        responses={200: ProductSerializer(many=False)},
        description="Update product",
        summary="Update product",
        tags=["Products"],
        deprecated=True,
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        operation_id="partial_update_product",
        request=ProductSerializer(),
        responses={200: ProductSerializer(many=False)},
        description="partial update product",
        summary="Partial update product",
        tags=["Products"],
    )
    def partial_update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        operation_id="delete_product",
        responses={204: ProductSerializer(many=False)},
        description="Delete product",
        summary="Delete product",
        tags=["Products"],
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
