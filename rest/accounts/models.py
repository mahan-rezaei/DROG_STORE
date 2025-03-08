from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
from django.utils.timezone import now
from datetime import timedelta
import secrets
import string


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField()
    phone_number = models.CharField(max_length=11, unique=True)
    full_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ('email', 'full_name')

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin
    

class OTP(models.Model):
    phone_number = models.CharField(max_length=11)
    code = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f'{self.phone_number} {self.code}'

    @staticmethod
    def create_otp(phone_number, length=8):
        characters = string.digits
        otp_code = ''.join(secrets.choice(characters) for _ in range(length))
        expiry_time = now() + timedelta(minutes=3)
        otp = OTP.objects.create(phone_number=phone_number, code=otp_code, expires_at=expiry_time)
        return otp_code
    
    @staticmethod
    def verify_otp(phone_number, enterd_code):
        otp = OTP.objects.filter(phone_number=phone_number, code=enterd_code,  expires_at__gte=now()).first()
        if otp:
            otp.delete()
            return True
        return False


