from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import viewsets, filters, status
from dateutil.relativedelta import relativedelta
from django.template.loader import render_to_string
from sistema import settings
from .serializer import UserSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
import threading
from .models import UsuarioExtendido
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import date, timedelta
from django.utils import timezone
from Task.task import usuarios_mayores_de_18_con_ti, enviar_correoCambioPsswrd, verificar_usuarios_inactivos


def iniciar_schedulerCambioDcmnto():
    scheduler = BackgroundScheduler()
    scheduler.add_job(usuarios_mayores_de_18_con_ti,  'interval', minutes=60)
    scheduler.start()
    print("Scheduler iniciado")


iniciar_schedulerCambioDcmnto()

def iniciar_cambioPsswrd():
    scheduler = BackgroundScheduler()
    scheduler.add_job(enviar_correoCambioPsswrd,  'interval', minutes=60)
    scheduler.start()
    print("Scheduler iniciado cambio password")


iniciar_cambioPsswrd()

def iniciar_usuarioBloqueado():
    scheduler = BackgroundScheduler()
    scheduler.add_job(verificar_usuarios_inactivos, 'cron', day_of_week='mon', hour=15, minute=18)
    scheduler.start()
    print("Scheduler iniciado verificar usuarios inactivos")
iniciar_usuarioBloqueado()

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
        if UsuarioExtendido.objects.filter(email=request.data.get('email')).exists():
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

