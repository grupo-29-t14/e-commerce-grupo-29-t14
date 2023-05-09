from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Address
from .serializers import AddressSerializer
from rest_framework.generics import UpdateAPIView, RetrieveAPIView, CreateAPIView
from .permissions import AddressPermisson, createAddressPermission
from drf_spectacular.utils import extend_schema


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

    @extend_schema(
        operation_id="create_address",
        request=AddressSerializer,
        responses={201: AddressSerializer},
        description="Route for creating a new address",
        summary="Address Creation",
        tags=["Address"],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    @extend_schema(
        operation_id="get_address",
        responses={200: AddressSerializer},
        description="Route for getting an address",
        summary="Address Retrieval",
        tags=["Address"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class UpdateAddressView(UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, AddressPermisson]

    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    @extend_schema(operation_id="deprecated_address_route", tags=["Address"], deprecated=True)
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        operation_id="partial_update_address",
        request=AddressSerializer,
        responses={200: AddressSerializer},
        description="Route for partially updating address information",
        summary="Partial address update",
        tags=["Address"],
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)
