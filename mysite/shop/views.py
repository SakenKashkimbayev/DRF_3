from django.contrib.auth import get_user_model
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, mixins, permissions, authentication, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from shop.models import Category, Product, Order, Warehouse
from shop.serializers import ProductSerializers, CategorySerializers, OrderSerializers, OrderDetailSerializers


# Для не авторизованных
class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers


class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers

    def get_queryset(self):
        queryset = super().get_queryset()
        filter_param1 = self.request.query_params.get('category')
        if filter_param1:
            queryset = queryset.filter(category=filter_param1)
        return queryset

class OrderListView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializers

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    def get_queryset(self):
        queryset = super().get_queryset()
        filter_param1 = self.request.query_params.get('status_order')
        if filter_param1:
            queryset = queryset.filter(status_order=filter_param1)
        return queryset

class OrderDetailView(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializers

class CategoryCRUDView(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      generics.GenericAPIView
                      ):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers

    # authentication_classes = [authentication.SessionAuthentication]
    # permission_classes = [permissions.DjangoModelPermissions]
    def get(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            return super().update(request, *args, **kwargs)
        return super().create(request, *args, **kwargs)


class ProductCRUDView(mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.RetrieveModelMixin,
                      generics.GenericAPIView
                      ):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers

    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.DjangoModelPermissions]

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            try:
                # Находим объект Warehouse по product_id равному pk
                warehouse = Warehouse.objects.get(product_id=pk)
                # Получаем нужные данные из объекта Warehouse
                warehouse_data = warehouse.total_quantity

                # Получаем данные о продукте
                product = self.get_object()
                product.warehouse_data = warehouse_data
                serializer = self.get_serializer(product)
                return Response(serializer.data)
            except Warehouse.DoesNotExist:
                # Если объект Warehouse с заданным product_id не найден, возвращаем 404
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return super().retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            return super().update(request, *args, **kwargs)
        # return super().create(request, *args, **kwargs)

