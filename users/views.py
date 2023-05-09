from rest_framework import generics, permissions
from rest_framework.response import Response
from users.serializers import UserSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import User
from .permissions import IsAdminOrAccountOwner
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.shortcuts import get_object_or_404


@extend_schema(
    request=TokenObtainPairSerializer,
    responses={200: TokenObtainPairSerializer},
    description="Route for obtaining an access and refresh token pair",
    summary="Login user and get access and refresh Token Obtainment",
    tags=["Login"],
)
class CustomizedTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


class UserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()

        return User.objects.filter(is_seller=True, is_active=True)

    @extend_schema(
        operation_id="users_list",
        responses={200: UserSerializer},
        description="Route for listing users",
        summary="List of Users",
        tags=["Users"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        operation_id="create_user",
        request=UserSerializer,
        responses={201: UserSerializer},
        description="Route for creating a new user",
        summary="User Creation",
        tags=["Users"],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrAccountOwner]

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_url_kwarg = "pk"

    @extend_schema(
        operation_id="delete_user",
        responses={204: "No Content"},
        description="Route for deleting a user",
        summary="User Deletion",
        tags=["Users"],
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_active is False:
            return Response(data={"message": "User already inactive"}, status=400)
        self.perform_destroy(instance)
        return Response(status=204)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    @extend_schema(
        operation_id="partial_update_user",
        request=UserSerializer,
        responses={200: UserSerializer},
        description="Route for partially updating user information",
        summary="Partial User Update",
        tags=["Users"],
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        operation_id="retrieve_user",
        responses={200: UserSerializer},
        description="Route for retrieving a user",
        summary="User Retrieval",
        tags=["Users"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        operation_id="Reactivate user",
        responses={
            200: {"message": "User activated"},
            400: {"message": "User already active"},
        },
        description="Route for reactivating a user",
        summary="Admin only - User Reactivation",
        tags=["Users"],
    )
    def put(self, request, *args, **kwargs):
        self.permission_classes = [permissions.IsAdminUser]
        user_to = get_object_or_404(User, pk=kwargs["pk"])
        if user_to.is_active:
            return Response(data={"message": "User already active"}, status=400)

        user_to.is_active = True
        user_to.save()

        return Response(data={"message": "User activated"}, status=200)
