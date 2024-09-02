from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import ValidationError


class UsuarioExtendido(AbstractUser):
    tipo_documento = models.CharField(max_length=3, blank=True, null=True)
    numero_documento = models.CharField(max_length=13, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    fecha_ultima_contrasenna = models.DateField(blank=True, null=True)
   

    # Sobrescribe el método para evitar que usuarios bloqueados inicien sesión
    def clean(self):
        if self.is_locked:
            raise ValidationError("Esta cuenta está bloqueada.")

# Create your models here.
