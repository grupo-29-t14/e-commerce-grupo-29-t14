from rest_framework import generics, permissions, response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from products.models import Product
from . import models
from . import serializers


class CartView(generics.CreateAPIView, generics.RetrieveAPIView):
    queryset = models.Cart.objects.all()
    serializer_class = serializers.CartSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    lookup_field = "buyer_id"

    def create(self, request, *args, **kwargs):
        data = request.data
        data.update({"buyer_id": str(self.request.user.id)})
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=201, headers=headers)

    def perform_create(self, serializer):
        return serializer.save(buyer=self.request.user)

    def get_object(self):
        return self.queryset.get(buyer_id=self.request.user.id)

    @extend_schema(deprecated=True, tags=["Cart"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        operation_id="create_cart",
        request=serializers.CartSerializer,
        responses={201: serializers.CartSerializer},
        description='Route for creating cart. Must send key-value pair "buyer_id": "id" to create cart',
        summary="Create cart",
        tags=["Cart"],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CartProductView(generics.CreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = models.CartProducts
    serializer_class = serializers.CartProductSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        obj = get_object_or_404(Product, id=self.request.data.get("product"))

        return serializer.save(cart=self.request.user.cart, price=obj.price, product=obj)

    @extend_schema(
        operation_id="partial_update_cart_product",
        request=serializers.CartProductSerializer,
        responses={200: serializers.CartProductSerializer},
        description='Route for updating quantity on product. Must send key-value pair "operation": "sum" to increase quantity',
        summary="Update quantity on cart_product",
        tags=["Cart Product"],
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(deprecated=True, tags=["Cart Product"])
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        operation_id="add_product_to_cart",
        request=serializers.CartProductSerializer,
        responses={201: serializers.CartProductSerializer},
        description='Route for adding product to cart. Must send key-value pair "product": "id" to add product to cart',
        summary="Add product to cart",
        tags=["Cart Product"],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    @extend_schema(
        operation_id="retrieve_product_from_cart",
        request=serializers.CartProductSerializer,
        responses={200: serializers.CartProductSerializer},
        description='Route for retrieving product from cart. Must send key-value pair "product": "id" to retrieve product from cart',
        summary="Retrieve product from cart",
        tags=["Cart Product"],
    )
    def get(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        operation_id="delete_cart_product",
        request=serializers.CartProductSerializer,
        responses={204: serializers.CartProductSerializer},
        description='Route for deleting product from cart. Must send key-value pair "product": "id" to delete product from cart',
        summary="Delete product from cart",
        tags=["Cart Product"],
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
