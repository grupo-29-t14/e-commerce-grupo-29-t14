from rest_framework import generics, permissions, response
from rest_framework_simplejwt.authentication import JWTAuthentication
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
        return self.queryset.get(buyer_id=self.request.user.pk)
