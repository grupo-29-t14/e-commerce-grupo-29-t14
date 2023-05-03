from rest_framework.generics import ListCreateAPIView
from .models import Product


class ProductView(ListCreateAPIView):
    queryset = Product.objects.all()
