from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrAdmin, IsOwner, IsSeller
from drf_spectacular.utils import extend_schema
from drf_spectacular.openapi import OpenApiParameter, OpenApiTypes
from djmoney.money import Money


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
            self.permission_classes = [IsSeller]
        else:
            self.permission_classes = [IsAuthenticatedOrReadOnly]
        return super(ProductViewSet, self).get_permissions()

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

    @extend_schema(
        operation_id="Retrieve_a_list_of_products",
        parameters=[
            OpenApiParameter(
                name="name",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Name of the product",
            ),
            OpenApiParameter(
                name="category",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Category of the product",
            ),
            OpenApiParameter(
                name="price",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Maximum price of the product",
            ),
        ],
        responses={200: ProductSerializer(many=True)},
        description="Retrieve all profucts or a list of products by name, category or price",
        summary="Retrieve a list of products",
        tags=["Products"],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        category_parameter = self.request.query_params.get("category", "")
        name_parameter = self.request.query_params.get("name", "")
        price_parameter = self.request.query_params.get("price", "")

        if price_parameter:
            queryset = Product.objects.filter(price__lte=Money(price_parameter, "BRL"))
            return queryset

        if category_parameter or name_parameter:
            queryset = Product.objects.filter(
                category__contains=category_parameter,
                name__contains=name_parameter,
            )
            if price_parameter:
                queryset = Product.objects.filter(
                    category__contains=category_parameter,
                    name__contains=name_parameter,
                    price__lte=Money(price_parameter, "BRL"),
                )
            return queryset

        return super().get_queryset()

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
