from django.core.mail import send_mail
from django.conf import settings
from datetime import date, timedelta
from django.utils import timezone
from .models import UsuarioExtendido
def enviar_correoCambioDcmnto(usuario):
    try:
        asunto = 'Notificación de Usuario'
        mensaje = f'Hola {usuario.username},\n\nEste es un recordatorio para que actualice su tipo de documento {usuario.tipo_documento} a C.C'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [usuario.email]
        send_mail(asunto, mensaje, email_from, recipient_list)
        print(f'Correo enviado a: {usuario.email}')
    except Exception as e:
        print(f'Error al enviar correo a {usuario.email}: {e}')
    
def usuarios_mayores_de_18_con_ti():
    print("Ejecutando la función de usuarios mayores de 18")
    hoy = timezone.now().date()
    edad_minima = hoy - timedelta(days=18*365.25)  # Aproximado para 18 años
    usuarios = UsuarioExtendido.objects.filter(
        tipo_documento='T.I',
        fecha_nacimiento__lte=edad_minima
    )
    
    if not usuarios:
        print("No se encontraron usuarios que cumplan con el criterio.")
    
    for usuario in usuarios:
        enviar_correoCambioDcmnto(usuario)
        print(f'Correo enviado a: {usuario.username}, Tipo Documento: {usuario.tipo_documento}, Fecha de Nacimiento: {usuario.fecha_nacimiento}')
        

def obtener_usuarios_para_cambio_password():
    hoy = timezone.now().date()
    # Por ejemplo, supongamos que la contraseña debe cambiarse cada 90 días
    fecha_limite = hoy - timedelta(days=1)
    usuarios = UsuarioExtendido.objects.filter(
        date_joined=fecha_limite
    )
    return usuarios
def enviar_correoCambioPsswrd():
    usuarios = obtener_usuarios_para_cambio_password()
    
    for usuario in usuarios:
        try:
            
            asunto = 'Notificación de Cambio de Contraseña'
            mensaje = (
                f'Hola {usuario.username},\n\n'
                f'Este es un recordatorio para que actualices tu contraseña.\n'
                
            )
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [usuario.email]
            send_mail(asunto, mensaje, email_from, recipient_list)
            print(f'Correo enviado a: {usuario.email}')
        except Exception as e:
            print(f'Error al enviar correo a {usuario.email}: {e}')
    print("Ejecutando la función de cambiar password")
    