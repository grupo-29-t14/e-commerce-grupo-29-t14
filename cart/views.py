from rest_framework import generics, permissions, response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from products.models import Product
from . import models
from . import serializers
from .permissions import IsAdminOrCartOwner


class CartView(generics.CreateAPIView, generics.RetrieveAPIView):
    queryset = models.Cart.objects.all()
    serializer_class = serializers.CartSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsAdminOrCartOwner]

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

    def get_queryset(self):
        if self.request.user.is_superuser:
            return models.Cart.objects.all()
        return models.Cart.objects.filter(buyer=self.request.user)

class CartProductView(generics.CreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = models.CartProducts
    serializer_class = serializers.CartProductSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsAdminOrCartOwner]

    def perform_create(self, serializer):
        obj = get_object_or_404(Product, id=self.request.data.get("product"))

        return serializer.save(
            cart=self.request.user.cart, price=obj.price, product=obj
        )

    @extend_schema(
        operation_id="partial_update_cart_product",
        request=serializers.CartProductSerializer,
        responses={200: serializers.CartProductSerializer},
        description='Route for updating quantity on product. Must send key-value pair "operation": "sum" to increase quantity',
        summary="Update quantity on cart_product",
        tags=["cart_product"],
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

class ListAllCartsView(generics.ListAPIView):
    queryset = models.Cart.objects.all()
    serializer_class = serializers.CartSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsAdminOrCartOwner]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return models.Cart.objects.all()
        return models.Cart.objects.none()
    
    def list(self, request, *args, **kwargs):
        if request.user.is_superuser:
            cart_id = request.query_params.get('id')
            if cart_id:
                queryset = self.get_queryset().filter(id=cart_id)
                serializer = self.get_serializer(queryset, many=True)
                return response.Response(serializer.data)
            return super().list(request, *args, **kwargs)
        return response.Response(status=403, data={"detail": "You do not have permission to perform this action."})