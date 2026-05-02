"""
Configuración de la aplicación 'socios' del proyecto Django.

Define parámetros transversales para todo el módulo responsable
de la interacción directa con el usuario, inscripciones y solicitudes de contacto.
"""

from django.apps import AppConfig


class SociosConfig(AppConfig):
    """
    Clase de inicialización para la aplicación 'socios'.

    Attributes:
        default_auto_field (str): Tipo de campo autoincremental para las Primary Keys.
        name (str): Ruta principal de acceso al módulo (requerido por Django).
    """
    
    # Utilizar BigAutoField asegura un límite máximo de identificadores primarios (IDs)
    # virtualmente inagotable, previniendo caídas del sistema si la tabla de solicitudes 
    # de contacto o de inscripción de socios crece exponencialmente a través de los años.
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Se incluye el prefijo 'apps.' obedeciendo a un diseño de arquitectura limpia (Clean Architecture)
    # que agrupa las aplicaciones dentro de una subcarpeta, evitando ensuciar el directorio raíz del proyecto.
    name = 'apps.socios'

