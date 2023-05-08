from django.urls import path
from .views import AddressView, UpdateAddressView, AddressView

urlpatterns = [
    path("address/<pk>", AddressView.as_view()),
    path("address/update/<pk>", UpdateAddressView.as_view()),
]
