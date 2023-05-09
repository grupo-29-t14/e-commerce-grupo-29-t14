from django.core.management import call_command
from django.core.management.base import CommandError
import json
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import generics
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
        self.authentication_classes = [JWTAuthentication]

        if not self.request.user.is_staff:
            return Response(
                status=400,
                data={"detail": "You do not have permission to perform this action."},
            )

        user_to = get_object_or_404(User, pk=kwargs["pk"])
        if user_to.is_active:
            return Response(data={"message": "User already active"}, status=400)

        user_to.is_active = True
        user_to.save()

        return Response(data={"message": "User activated"}, status=200)


class CreateAdminView(APIView):
    @extend_schema(
        operation_id="create_admin",
        description="Route for creating a new admin for testing purposes. Username is 'admin', password is 'admin1234'",
        tags=["Users"],
        # exclude=True
    )
    def post(self, request, *args, **kwargs):
        admin_username = "admin"
        admin_password = "admin1234"
        admin_email = f"{admin_username}@example.com"

        if request.body:
            data = json.loads(request.body)
            admin_username = data.get("username", admin_username)
            admin_password = data.get("password", admin_password)
            admin_email = data.get("email", admin_email)

        check_username = User.objects.filter(username=admin_username).first()
        check_email = User.objects.filter(email=admin_email).first()

        if check_username:
            return JsonResponse(
                {"error": f"Username '{check_username.username}' already taken."},
                status=400,
            )
        if check_email:
            return JsonResponse(
                {"error": f"Email '{check_email.email}' already taken."}, status=400
            )

        options = {
            "username": admin_username,
            "password": admin_password,
            "email": admin_email,
        }

        try:
            call_command("create_admin", **options)
            return JsonResponse(
                {"message": "Superuser created successfully!"}, status=201
            )
        except CommandError as e:
            return JsonResponse({"error": str(e)}, status=400)


class CreateAdminView(APIView):
    @extend_schema(
        operation_id="create_admin",
        description="Route for creating a new admin for testing purposes. Username is 'admin', password is 'admin1234'",
        tags=["Users"],
        # exclude=True
    )
    def post(self, request, *args, **kwargs):
        admin_username = "admin"
        admin_password = "admin1234"
        admin_email = f"{admin_username}@example.com"

        if request.body:
            data = json.loads(request.body)
            admin_username = data.get("username", admin_username)
            admin_password = data.get("password", admin_password)
            admin_email = data.get("email", admin_email)

        check_username = User.objects.filter(username=admin_username).first()
        check_email = User.objects.filter(email=admin_email).first()

        if check_username:
            return JsonResponse(
                {"error": f"Username '{check_username.username}' already taken."},
                status=400,
            )
        if check_email:
            return JsonResponse(
                {"error": f"Email '{check_email.email}' already taken."}, status=400
            )

        options = {
            "username": admin_username,
            "password": admin_password,
            "email": admin_email,
        }

        try:
            call_command("create_admin", **options)
            return JsonResponse(
                {"message": "Superuser created successfully!"}, status=201
            )
        except CommandError as e:
            return JsonResponse({"error": str(e)}, status=400)
