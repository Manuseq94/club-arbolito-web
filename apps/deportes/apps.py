"""
Configuración de la aplicación 'deportes' del proyecto Django.

Este módulo se encarga de registrar la aplicación en el proyecto y definir 
configuraciones de inicialización como el tipo de campo auto-incremental por defecto.
"""

from django.apps import AppConfig


class DeportesConfig(AppConfig):
    """
    Clase de configuración principal para la aplicación 'deportes'.

    Attributes:
        default_auto_field (str): Tipo de campo definido para las claves primarias (PK).
        name (str): Ruta completa de la aplicación dentro del proyecto.
    """
    
    # Se utiliza BigAutoField para prevenir que a futuro se agote el espacio 
    # disponible de IDs enteros limitados en caso de alto volumen de datos.
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Se define la ruta con el prefijo 'apps.' debido a que el proyecto utiliza 
    # un patrón de diseño donde las aplicaciones están agrupadas en ese directorio.
    name = 'apps.deportes'
