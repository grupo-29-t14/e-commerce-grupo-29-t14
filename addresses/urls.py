from django.urls import path
from .views import AddressView, UpdateAddressView

urlpatterns = [
    path("address/", AddressView.as_view()),
    path("address/update/<pk>", UpdateAddressView.as_view()),
]
