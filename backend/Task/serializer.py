from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UsuarioExtendido  

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioExtendido
        fields = ['id', 'username', 'email', 'password', 'tipo_documento', 'numero_documento', 'fecha_nacimiento']

    def create(self, validated_data):
        user = UsuarioExtendido.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            tipo_documento=validated_data.get('tipo_documento', ''),
            numero_documento=validated_data.get('numero_documento', ''),
            fecha_nacimiento=validated_data.get('fecha_nacimiento', None)
        )
        return user