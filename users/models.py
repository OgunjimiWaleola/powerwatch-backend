from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    email = models.EmailField(
        unique=True,
        blank=True,
        null=True
    )

    phone_number = PhoneNumberField(
        unique=True,
        null=True,
        blank=True
    )

    full_name = models.CharField(
        max_length=150,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone_number.as_e164 if self.phone_number else self.username
