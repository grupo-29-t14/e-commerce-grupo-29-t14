from django.urls import path
from . import views
from .views import ListAllCartsView


urlpatterns = [
    path('carts/all/', views.ListAllCartsView.as_view(), name='list_all_carts'),
]
