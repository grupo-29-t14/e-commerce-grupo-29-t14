from django.urls import path
from .views import ProductGetView, ProductCreateView, ProductUpdateView, ProductDeleteView

urlpatterns = [
    path('products/', ProductGetView.as_view(), name='product-list'),
    path('products/create/', ProductCreateView.as_view(), name='product-create'),
    path('products/<uuid:id>/', ProductUpdateView.as_view(), name='product-update'),
    path('products/<uuid:id>/delete/', ProductDeleteView.as_view(), name='product-delete')
]


