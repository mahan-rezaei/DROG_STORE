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
    phone_numebr = models.CharField(max_length=11)
    code = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    expiers_at = models.DateTimeField()

    @staticmethod
    def create_otp(phone_numebr, length=8):
        characters = string.ascii_uppercase + string.digits
        otp_code = ''.join(secrets.choice(characters) for _ in range(length))
        expiry_time = now() + timedelta(minutes=3)
        otp = OTP.objects.create(phone_numebr=phone_numebr, code=otp_code, expiers_at=expiry_time)
        return otp_code
    
    @staticmethod
    def verify_otp(phone_numebr, enterd_code):
        otp = OTP.objects.filter(phone_numebr=phone_numebr, code=enterd_code,  expires_at__gte=now()).first()
        if otp:
            otp.delete()
            return True
        return False


