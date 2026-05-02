"""
Procesadores de contexto globales para la aplicación 'deportes'.
"""

from django.core.cache import cache

from .models import Disciplina


def disciplinas_globales(request):
    """
    Inyecta la lista de disciplinas en el contexto general de las plantillas.

    Se ejecuta automáticamente en cada renderizado (usualmente para popular
    el menú de navegación de base.html). Implementa un sistema de caché 
    para evitar golpear la base de datos de manera excesiva.

    Args:
        request (HttpRequest): Objeto de petición actual de Django.

    Returns:
        dict: Diccionario que contiene las disciplinas bajo la llave 'menu_disciplinas'.
    """
    cache_key = 'menu_disciplinas_global'
    
    # Optimización: Obtener datos del caché RAM en vez de la DB.
    # Dado que este procesador corre en CADA petición HTTP de los usuarios, 
    # hacer una llamada .all() a la BD constamente crea un cuello de botella severo.
    disciplinas = cache.get(cache_key)
    
    if disciplinas is None:
        # Optimización: Usamos .only() para pedirle a la base de datos únicamente 
        # las columnas puntuales que un menú desplegable de navegación necesita,
        # ahorrando transferencia de texto y procesamiento extra (ej: no trae descripciones).
        disciplinas = list(Disciplina.objects.only('id', 'nombre', 'slug').order_by('nombre'))
        
        # Guardamos en caché por 24 horas (86400 segundos).
        # (Idealmente, este caché se invalida por señales al crear/borrar Disciplinas).
        cache.set(cache_key, disciplinas, 86400)

    return {'menu_disciplinas': disciplinas}
