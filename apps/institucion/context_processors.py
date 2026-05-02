"""
Procesadores de contexto globales para la aplicación 'institucion'.
"""

from django.core.cache import cache

from .models import Categoria


def categorias_globales(request):
    """
    Inyecta la lista de categorías en el contexto general de las plantillas.

    Al igual que en la app de deportes, este procesador se ejecuta en TODAS 
    las peticiones HTTP (usualmente para popular el menú de navegación general 
    de base.html). Incluye caché para proteger la base de datos de cargas masivas.

    Args:
        request (HttpRequest): Objeto de petición actual de Django.

    Returns:
        dict: Diccionario que contiene las categorías bajo la llave 'menu_categorias'.
    """
    cache_key = 'menu_categorias_global'
    
    # Optimización Crítica: Al procesarse en el 100% de las páginas cargadas por 
    # todos los usuarios concurrentes, golpearía constantemente la BD con lecturas repetidas. 
    # Extraer el resultado de la memoria RAM (caché) previene este desastre de escalabilidad.
    categorias = cache.get(cache_key)
    
    if categorias is None:
        # Optimización Activa (.only): Excluye de las columnas descargadas cualquier 
        # data pesada, trayendo estrictamente 'nombre' y 'slug' para el enlace HTML.
        # Además instanciamos el queryset con list() para guardarlo plano y limpio en caché.
        categorias = list(Categoria.objects.only('id', 'nombre', 'slug').order_by('nombre'))
        
        # Guardamos en caché por 24 horas (86400 segundos).
        cache.set(cache_key, categorias, 86400)

    return {'menu_categorias': categorias}
