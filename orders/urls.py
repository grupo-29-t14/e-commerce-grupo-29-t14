from django.urls import path
from .views import OrderView, RetriveOrderView, ListOrderView, DestroyOrderView, UpdateOrderView, ListOrdersBySeller

urlpatterns = [
    path("orders/", OrderView.as_view()),
    path("orders/user/<str:pk>/", ListOrderView.as_view()),
    path("orders/<str:pk>/", RetriveOrderView.as_view()),
    path("orders/delete/<str:pk>/", DestroyOrderView.as_view()),
    path("orders/update/<str:pk>/", UpdateOrderView.as_view()),
    path("orders/seller/<str:pk>", ListOrdersBySeller.as_view())
]
