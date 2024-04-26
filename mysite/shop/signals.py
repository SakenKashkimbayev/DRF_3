from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from shop.models import Cart
from authorization.models import User
# Получаем модель пользователя
# User = get_user_model()

# Обработчик сигнала
@receiver(post_save, sender=User)
def create_user_cart(sender, instance, created, **kwargs):
    if created:  # Проверяем, был ли создан новый пользователь
        Cart.objects.create(user=instance)
        Cart.save()