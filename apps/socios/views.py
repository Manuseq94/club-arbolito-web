"""
Lógica central de presentación para la aplicación 'socios'.

Maneja los procesos de inscripción de usuarios y la recepción
de consultas generales, respetando los patrones de seguridad de HTTP.
"""

from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import SolicitudSocioForm
from .models import ConsultaContacto


def hazte_socio(request):
    """
    Gestiona el formulario interactivo para la afiliación de nuevos socios.

    Soporta el renderizado neutro (GET) y la ingesta estructural de datos (POST)
    pasando estrictamente por las validaciones seguras de `SolicitudSocioForm`.

    Args:
        request (HttpRequest): Petición actual recibida por el servidor.

    Returns:
        HttpResponse: Formulario reactivo o redirección de éxito.
    """
    if request.method == 'POST':
        form = SolicitudSocioForm(request.POST)
        
        # is_valid() evalúa en memoria RAM si la data enviada por el navegador 
        # cumple los requisitos (longitud, inyección SQL, protección CSRF y formato mail).
        if form.is_valid():
            form.save()
            
            # Inyección de Estado Efímero (Flash Messaging): Usamos la sesión del user 
            # para mandar una alerta de éxito flotante en la UI del siguiente render.
            messages.success(request, '¡Tu solicitud fue enviada con éxito! Nos contactaremos a la brevedad.')
            
            # Arquitectura HTTP (Patrón PRG: Post-Redirect-Get): Fundamental redirigir  
            # tras guardar datos. Evita el infame bug de la web donde el usuario recarga 
            # la página con F5 y duplica permanentemente el insert en la base de datos.
            return redirect('socios:hazte_socio')
    else:
        form = SolicitudSocioForm()

    return render(request, 'hazte_socio.html', {'form': form})


def contacto_admin(request):
    """
    Endpoint mixto que renderiza el contacto de la institución y 
    procesa la ingesta de dudas libres de los usuarios.

    Args:
        request (HttpRequest): Petición recibida.
    """
    if request.method == 'POST':
        # Arquitectura Pobre / Lógica Cruda: Extraer datos directamente del POST 
        # y guardarlos con .create() asume que el Frontend sanitizará todo.
        # Deuda Técnica a reparar: Mover todo esto a un "ConsultaContactoForm" (ModelForm) 
        # para delegar la limpieza, la inyección y el chequeo al Backend robusto de Django.
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        mensaje_texto = request.POST.get('mensaje')

        ConsultaContacto.objects.create(
            nombre_usuario=nombre,
            email=email,
            telefono=telefono,
            mensaje=mensaje_texto
        )
        
        messages.success(request, "¡Tu consulta fue enviada! Nos pondremos en contacto pronto.")
        
        # Se replica el Patrón PRG para evitar que F5 clave de nuevo el comentario.
        return redirect('socios:contacto_admin')

    return render(request, 'contacto_admin.html')


# --- Vistas Estáticas Informativas ---

def info_cuotas(request):
    """Renderiza el display tarifario y los métodos automáticos de pago."""
    return render(request, 'info_cuotas.html')


def info_socios(request):
    """Renderiza portal institucional de beneficios puros de ser miembro activo."""
    return render(request, 'info_socios.html')
