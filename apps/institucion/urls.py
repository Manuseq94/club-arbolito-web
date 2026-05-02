"""
Configuración de rutas (URLs) para la aplicación 'institucion'.

Mapea todas las secciones estáticas y dinámicas centrales del club,
desde la página de inicio (Home) hasta los artículos de noticias y
toda la información de recorrido institucional.
"""

from django.urls import path

from . import views


# Namespace (espacio de nombres) para aislar las vistas de la institución.
# Previene colisiones críticas de nombrado de URLs en los templates HTML 
# (ej: evita choques entre 'institucion:inicio' y un potencial 'ecommerce:inicio').
app_name = 'institucion' 

urlpatterns = [
    # --- Vistas Generales ---
    path('', views.inicio, name='inicio'),
    path('noticias/', views.noticias_list, name='noticias_list'),
    
    # Nota Arquitectónica (Deuda Técnica SEO): Se mantiene el localizador por 
    # ID numérico (<int:noticia_id>) por compatibilidad en la lógica actual de vistas. 
    # Recomendado migrar a 'slug' en el futuro para elevar el rankeo orgánico en Google.
    path('noticia/<int:noticia_id>/', views.noticia_detalle, name='noticia_detalle'),
    
    # --- Secciones del Club ---
    path('el-club/historia/', views.historia, name='historia'),
    path('el-club/galeria/', views.galeria, name='galeria'),
    path('el-club/sede-social/', views.sede_social, name='sede_social'),
    path('el-club/comision-directiva/', views.comision_directiva, name='comision_directiva'),
    
    # --- Legales y Políticas ---
    path('terminos-y-condiciones/', views.terminos_condiciones, name='terminos'),
    path('politicas-de-privacidad/', views.politicas_privacidad, name='privacidad'),
]

