from django.urls import path
from .views import AddressView, UpdateAddressView, AddressView

urlpatterns = [
    path("address/<str:pk>/", AddressView.as_view()),
    path("address/update/<str:pk>/", UpdateAddressView.as_view()),
]
