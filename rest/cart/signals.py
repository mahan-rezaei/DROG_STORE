from django.contrib.auth import get_user_model
from .models import Cart
from django.dispatch import receiver
from django.db.models.signals import post_save


User = get_user_model()

@receiver(post_save, sender=User)
def create_cart_for_new_user(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)