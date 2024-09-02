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
    # La contraseña debe cambiarse si no se ha actualizado en los últimos 5 días
    fecha_limite = hoy - timedelta(days=5)
    usuarios = UsuarioExtendido.objects.filter(
        fecha_ultima_contrasenna=fecha_limite
    )
    return usuarios

def enviar_correoCambioPsswrd():
    usuarios = obtener_usuarios_para_cambio_password()
    
    for usuario in usuarios:
        try:
            asunto = 'Notificación de Cambio de Contraseña'
            mensaje = (
                f'Hola {usuario.username},\n\n'
                f'Este es un recordatorio para que actualices tu contraseña, ya que no ha sido cambiada en los últimos 5 días.\n'
            )
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [usuario.email]
            send_mail(asunto, mensaje, email_from, recipient_list)
            print(f'Correo enviado a: {usuario.email}')
        except Exception as e:
            print(f'Error al enviar correo a {usuario.email}: {e}')
    print("Ejecutando la función de enviar correos para cambio de contraseña")
    
def verificar_usuarios_inactivos():
    # Obtener fecha límite de un mes
    hace_un_mes = timezone.now() - timedelta(days=30)

    # Buscar usuarios que no han iniciado sesión hace más de un mes y que están activos
    usuarios_a_bloquear = UsuarioExtendido.objects.filter(last_login__lt=hace_un_mes, is_active=1)


    # Verificar si se encontraron usuarios
    if not usuarios_a_bloquear.exists():
        print("No se encontraron usuarios inactivos para bloquear.")
    else:
        print(f"Usuarios encontrados para bloquear: {usuarios_a_bloquear.count()}")
        for usuario in usuarios_a_bloquear:
            print(f"Usuario: {usuario.username}, Último inicio de sesión: {usuario.last_login}, Email: {usuario.email}")

    for usuario in usuarios_a_bloquear:
        try:
            # Bloquear usuario marcándolo como inactivo
            usuario.is_active = 0
            usuario.save()

            # Enviar correo de notificación
            asunto = 'Cuenta bloqueada por inactividad'
            mensaje = (
                f'Hola {usuario.username},\n\n'
                'Tu cuenta ha sido bloqueada debido a la inactividad prolongada. '
                'Si necesitas ayuda o crees que esto es un error, por favor contacta con soporte.'
            )
            email_from = settings.EMAIL_HOST_USER  # Usa el email configurado en settings
            recipient_list = [usuario.email]

            send_mail(asunto, mensaje, email_from, recipient_list, fail_silently=False)
            print(f'Correo enviado a: {usuario.email}')
        except Exception as e:
            print(f'Error al enviar correo a {usuario.email}: {e}')

    print("Verificación de usuarios inactivos completada.")