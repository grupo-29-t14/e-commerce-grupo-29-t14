from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Address
from .serializers import AddressSerializer
from rest_framework.generics import ListCreateAPIView, UpdateAPIView
from .permissions import AddressPermisson


class AddressView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def perform_create(self, serializer):
        user_id = self.request.user
        return serializer.save(user=user_id)

    def get_queryset(self):
        user_id = self.request.user.id
        return Address.objects.filter(user_id=user_id)


class UpdateAddressView(UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, AddressPermisson]

    queryset = Address.objects.all()
    serializer_class = AddressSerializer
