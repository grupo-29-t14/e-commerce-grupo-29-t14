from rest_framework import generics
from users.serializers import UserSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import User
from .permissions import IsAdminOrAccountOwner


class UserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = []

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
