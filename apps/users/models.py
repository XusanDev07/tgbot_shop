from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, telegram_id, password=None, **extra_fields):
        if not telegram_id:
            raise ValueError("Telegram ID bo'lishi shart.")
        user = self.model(telegram_id=telegram_id, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        return user

    def create_superuser(self, telegram_id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(telegram_id, password=password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    LANGUAGE_CHOICES = [
        ('uz', 'O‘zbek'),
        ('ru', 'Русский'),
    ]

    telegram_id = models.BigIntegerField(unique=True)
    full_name = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='uz')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'telegram_id'

    def __str__(self):
        return f"{self.full_name or 'Foydalanuvchi'} ({self.telegram_id})"
