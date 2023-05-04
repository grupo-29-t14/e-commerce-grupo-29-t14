from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views
from cart import views as cart_views

urlpatterns = [
    path("users/", views.UserView.as_view()),
    path("users/login/", jwt_views.TokenObtainPairView.as_view()),
    path("users/cart/", cart_views.CartView.as_view()),
    path("users/<str:pk>/", views.UserDetailView.as_view()),
]
