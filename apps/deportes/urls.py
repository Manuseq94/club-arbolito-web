"""
Configuración de rutas (URLs) para la aplicación 'deportes'.

Este módulo mapea las URLs front-end con las vistas (controladores) 
que resuelven la lógica y devuelven el HTML.
"""

from django.urls import path

from . import views


# Permite aislar estas rutas en el proyecto principal ('namespaces').
# Evita colisiones por si otra app tiene una ruta llamada también 'disciplina_detalle'.
# En los templates permite utilizar {% url 'deportes:disciplina_detalle' %}
app_name = 'deportes'

urlpatterns = [
    # Optimización/Diseño: Se utiliza un 'slug' de string (ej: /voley/) en vez de su 'id' 
    # numérico (ej: /3/). Esto fomenta el SEO (Search Engine Optimization) para indexación
    # y hace que las direcciones web sean descriptivas y amigables para los usuarios.
    path('<slug:slug>/', views.disciplina_detalle, name='disciplina_detalle'),
]