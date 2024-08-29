from django.db import models
from django.contrib.auth.models import AbstractUser


class UsuarioExtendido(AbstractUser):
    tipo_documento = models.CharField(max_length=3, blank=True, null=True)
    numero_documento = models.CharField(max_length=13, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)

# Create your models here.
