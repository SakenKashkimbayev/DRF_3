from django.contrib.auth import get_user_model
from django.db import models

from authorization.models import User


# Категория товара
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    registration_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    end_registration_date = models.DateTimeField(null=True, blank=True, verbose_name='Дата завершения регистрации')

    def __str__(self):
        return self.name

# Продукты привязанны к категории
class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    registration_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    end_registration_date = models.DateTimeField(null=True, blank=True, verbose_name='Дата завершения регистрации')

    def __str__(self):
        return self.name

# Корзина привязана к пользователю
class Cart(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, verbose_name='Пользователь')
    registration_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    products = models.ManyToManyField('Product', through='CartItem', verbose_name='Товары')

    def __str__(self):
        return f"Корзина пользователя {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='Корзина')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    def __str__(self):
        return f"{self.quantity} шт. {self.product.name} в корзине пользователя {self.cart.user.username}"

# Склад берет у продукта имя но в случае удаления продукта имя в складе остаеться
class Warehouse(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    total_quantity = models.PositiveIntegerField(default=0, verbose_name='Общее количество на складе')
    registration_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')

# Квитанция создается на каждую позицию в корзине отдельно
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    registration_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')

    def __str__(self):
        return f"Квитанция  {self.user.username}" \
               f"на товар {self.product}" \
               f"в количестве {self.quantity}"
