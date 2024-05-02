from django.contrib import admin
from django.urls import path

from shop import views
from shop.views import CategoryListView, ProductCRUDView, CategoryCRUDView, ProductListView, OrderListView, \
    OrderDetailView

urlpatterns = [
    path('product/', ProductListView.as_view()),
    path('product/<int:pk>/', ProductCRUDView.as_view()),
    path('order/', OrderListView.as_view()),
    path('order/<int:pk>/', OrderDetailView.as_view()),
    # для тестов
    path('createC/', CategoryListView.as_view()),
]
