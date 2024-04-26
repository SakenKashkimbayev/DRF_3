from django.contrib import admin
from django.urls import path

from shop import views
from shop.views import ProductCreateView, CategoryListView, ProductView, ProductCRUDView, CategoryCRUDView

urlpatterns = [
    path('', CategoryListView.as_view()),

    path('all/', ProductCRUDView.as_view()),
    path('all/<int:pk>/', ProductCRUDView.as_view()),

    path('createP/', ProductCreateView.as_view()),
    path('createC/', CategoryCRUDView.as_view()),
    path('<int:pk>/', ProductView.as_view()),
    # path('<int:pk>/update/', ProductUpdatelView.as_view()),
    # path('<int:pk>/archive/', ProductDetailView.as_view()),

    # path('', index),

]
