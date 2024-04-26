from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework import generics, mixins, permissions, authentication
from rest_framework.decorators import api_view
from rest_framework.response import Response

from shop.models import Category, Product
from shop.serializers import ProductSerializers, CategorySerializers


class ProductCreateView(generics.CreateAPIView):
    serializer_class = ProductSerializers

    def perform_create(self, serializer):
        serializer.save()


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers


class ProductView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers

    lookup_field = 'pk'

class CategoryCRUDView(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      generics.GenericAPIView
                      ):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers

    def get(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            return super().update(request, *args, **kwargs)
        return super().create(request, *args, **kwargs)


class ProductCRUDView(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      generics.GenericAPIView
                      ):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers

    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.DjangoModelPermissions]

    def get(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            return super().update(request, *args, **kwargs)
        return super().create(request, *args, **kwargs)


# class ProductUpdatelView(generics.UpdateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializers
#
#     lookup_field = 'pk'
#
# class ProductDetailView(generics.RetrieveAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializers
#
#     lookup_field = 'pk'















# @api_view(['GET', 'POST'])
# def index(request):
#     if request.method == "POST":
#         instance = ProductSerializers(data=request.data)
#
#         if instance.is_valid(raise_exception=True):
#             instance.save()
#
#             return Response(instance.data, status=status.HTTP_201_CREATED)
#
#     elif request.method == "GET":
#         product_id = request.GET.get('product_id')
#         product = Product.objects.get(pk=product_id)
#         data = {}
#         if product:
#             instance = ProductSerializers(product)
#
#             return Response(instance.data)
#         else:
#             return Response({'detail': 'Product not found', 'status': status.HTTP_404_NOT_FOUND})
