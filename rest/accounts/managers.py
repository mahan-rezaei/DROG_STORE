from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, full_name, phone_number, email, password):
        if not full_name:
            raise ValueError('Users must have full name')

        if not email:
            raise ValueError('Email must be set')

        if not phone_number:
            raise ValueError('Phone number must be set')

        norm_email = self.normalize_email(email)
        user = self.model(full_name=full_name, phone_number=phone_number, email=norm_email)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, full_name, phone_number, email, password):
        user = self.create_user(full_name, phone_number, email, password)
        user.is_admin = True
        user.is_superuser = True
        user.save()
        return user
