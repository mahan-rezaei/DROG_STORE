from django.db import models
from django.contrib.auth import get_user_model
from shop.models import Product
from django.utils import timezone

User = get_user_model()


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    title = models.CharField(max_length=100)  # عنوان آدرس (مثلاً: خانه، محل کار)
    receiver_name = models.CharField(max_length=100)
    receiver_phone = models.CharField(max_length=15)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    address = models.TextField()
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.is_default:
            # اگر این آدرس به عنوان پیش‌فرض انتخاب شده، سایر آدرس‌های کاربر را غیر پیش‌فرض می‌کنیم
            Address.objects.filter(user=self.user, is_default=True).exclude(id=self.id).update(is_default=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.title}"


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"cart for {self.user.phone_number}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cart} - {self.product} - {self.quantity}"
    

class DiscountCode(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount_percent = models.PositiveIntegerField()
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        now = timezone.now()
        return (
            self.is_active and
            self.valid_from <= now <= self.valid_until
        )

    def __str__(self):
        return f"{self.code} - {self.discount_percent}%"


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('shiped', 'Shiped'),
        ('deliverd', 'Deiliverd'),
        ('canceled', 'Canceled')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    address = models.ForeignKey(Address, on_delete=models.PROTECT)  # از PROTECT استفاده می‌کنیم تا اگر آدرس حذف شد، سفارش‌ها حفظ شوند
    total_price = models.PositiveBigIntegerField()
    discount_code = models.ForeignKey(DiscountCode, on_delete=models.SET_NULL, null=True, blank=True)
    discount_amount = models.PositiveBigIntegerField(default=0)
    final_price = models.PositiveBigIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.final_price}"
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.PositiveBigIntegerField()

    def __str__(self):
        return f"{self.quantity} X {self.product.name}"