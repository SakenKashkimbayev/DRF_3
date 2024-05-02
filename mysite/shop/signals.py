from django.db.models.signals import post_save
from django.dispatch import receiver
from shop.models import Product, Warehouse, Order
from django.db import transaction


# Обработчик сигнала
@receiver(post_save, sender=Product)
def create_product(sender, instance, created, **kwargs):
    if created:  # Проверяем, был ли создан новый пользователь
        Warehouse.objects.create(product=instance)

@receiver(post_save, sender=Order)
def process_order(sender, instance, created, **kwargs):
    # Проверяем, был ли создан новый заказ или изменен существующий
    if not created and instance.status_order == 2:
        product = instance.product
        quantity = instance.quantity
        print('количество в заказе', quantity)
        try:
            with transaction.atomic():
                # Получаем объект Warehouse для данного продукта
                warehouse = Warehouse.objects.get(product=product)
                print('количество на складе', warehouse.total_quantity)
                # Проверяем, достаточно ли товара на складе
                if warehouse.total_quantity >= quantity:
                    # Вычитаем количество товара из склада
                    warehouse.total_quantity -= quantity
                    warehouse.save()
                else:
                    # Если товара недостаточно, выбрасываем исключение
                    raise ValueError("Not enough product in stock")
        except Warehouse.DoesNotExist:
            # Если продукт отсутствует на складе, выбрасываем исключение
            raise ValueError("Product not found in warehouse")