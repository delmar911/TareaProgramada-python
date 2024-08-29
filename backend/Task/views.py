from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import viewsets, filters, status
from django.template.loader import render_to_string
from sistema import settings
from .serializer import UserSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
import threading
# Create your views here.


from django.core.mail import EmailMultiAlternatives

# Create your views here.

@api_view(['POST'])
def iniciarSesion(request):
    
    user = get_object_or_404(User, email=request.data['email'])
    
    if not user.check_password(request.data['password']):
        return Response({'error': 'Contraseña incorrecta'}, status=status.HTTP_401_UNAUTHORIZED)
    
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
     #aqui retorna el token
    return Response({"token": token.key}, status=status.HTTP_200_OK)

#registro de usuario
@api_view(['POST'])
def registro(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        print(request.data)
        # Verificar si el usuario ya existe por email
        if User.objects.filter(email=request.data.get('email')).exists():
            return Response({'error': 'El usuario ya se encuentra registrado'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(serializer.validated_data['password'])
            user.save()
            # Crea el token y lo guarda
            token = Token.objects.create(user=user)
            
            # Definir la función de envío de correo
            def send_email():
                subject = 'Bienvenid@ a Website'
                from_email = settings.EMAIL_HOST_USER
                to = request.data.get('email')
                text_content = 'Gracias por registrarte en Website.'
                html_content = render_to_string('correoRegistro.html', {'subject': subject, 'message': text_content})

                email = EmailMultiAlternatives(subject, text_content, from_email, [to])
                email.attach_alternative(html_content, "text/html")
                email.send()

            # Iniciar el envío del correo en un hilo separado
            email_thread = threading.Thread(target=send_email)
            email_thread.start()
            
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#acceso al perfil
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def perfil(request):
    
    return Response("Usted está iniciando sesión con {}".format(request.user.email), status=status.HTTP_200_OK)
