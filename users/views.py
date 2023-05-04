from rest_framework import generics
from rest_framework.response import Response
from users.serializers import UserSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import User
from .permissions import IsAdminOrAccountOwner


class UserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()

        return User.objects.filter(is_seller=True, is_active=True)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrAccountOwner]

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_url_kwarg = "pk"

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_active is False:
            return Response(data={"message": "User already inactive"}, status=400)
        self.perform_destroy(instance)
        return Response(status=204)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    def perform_update(self, serializer):
        if self.request.user.is_superuser is False and serializer.validated_data.get(
            "is_seller"
        ):
            serializer.validated_data.pop("is_seller", None)

        return super().perform_update(serializer)
