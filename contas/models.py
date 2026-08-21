from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):

    telefone = models.CharField(
        max_length=20,
        blank=True
    )

    is_admin_salao = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.username