from rest_framework.generics import ListCreateAPIView
from .models import User


class UserView(ListCreateAPIView):
    queryset = User.objects.all()
