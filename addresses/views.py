from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Address
from .serializers import AddressSerializer
from rest_framework.generics import UpdateAPIView, RetrieveAPIView, CreateAPIView
from .permissions import AddressPermisson, createAddressPermission


class AddressView(CreateAPIView, RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, AddressPermisson, createAddressPermission]

    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def perform_create(self, serializer):
        kwargs = self.kwargs
        serializer.save(user_id=kwargs["pk"])

    def get_queryset(self):
        kwargs = self.kwargs
        return Address.objects.filter(id=kwargs["pk"])


class UpdateAddressView(UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, AddressPermisson]

    queryset = Address.objects.all()
    serializer_class = AddressSerializer
