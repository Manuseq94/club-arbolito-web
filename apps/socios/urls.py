"""
Configuración de rutas (URLs) para la aplicación 'socios'.

Mapea funcionalmente las secciones ligadas a la suscripción de nuevos
miembros, las cuotas relativas al club y el portal general de contacto.
"""

from django.urls import path

from . import views


# El 'namespace' aisla internamente a la aplicación posibilitando 
# direccionar con robustez en los tags de HTML: {% url 'socios:hazte_socio' %}
# Previene colisiones con rutas llamadas "contacto" que existan o surjan en otras apps.
app_name = 'socios'

urlpatterns = [
    # Optimización/SEO Orgánico: Documento local que alinea en una muy buena práctica: 
    # Mantener estas URLs estáticas, breves, legibles y descriptivas (sin variables 
    # dinámicas ocultas referidas) puntúa sumamente alto en los algoritmos de accesibilidad.
    path('asociate/', views.hazte_socio, name='hazte_socio'),
    path('cuotas/', views.info_cuotas, name='info_cuotas'),
    path('informacion/', views.info_socios, name='info_socios'),
    path('contacto/', views.contacto_admin, name='contacto_admin'),
]