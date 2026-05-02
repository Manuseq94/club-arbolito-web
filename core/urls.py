from django.contrib import admin
from django.urls import path, include
from apps.institucion.views import inicio # Importamos nuestra vista
# Importamos estas dos librerías para manejar los archivos multimedia
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('panel-privado-directivos/', admin.site.urls),
    path('socios/', include('apps.socios.urls')),
    path('disciplinas/', include('apps.deportes.urls')),
    # Le decimos a Django: "Todo lo que no sea /admin, mandalo a las rutas de institucion"
    path('', include('apps.institucion.urls')),
]

# Le decimos a Django que sirva los archivos de la carpeta /media/ 
# SOLO cuando estamos en modo DEBUG (desarrollo local). En producción (Render) lo maneja otro servidor.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)