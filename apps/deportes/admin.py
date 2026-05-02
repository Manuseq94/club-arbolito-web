"""
Configuración del panel de administración para la aplicación 'deportes'.

Este módulo define cómo se registran y visualizan los modelos `Disciplina`,
`Partido` e `ImagenDisciplina` en la interfaz base de administración de Django.
"""

from django.contrib import admin

from .models import Disciplina, ImagenDisciplina, Partido


class ImagenDisciplinaInline(admin.TabularInline):
    """
    Inline para gestionar las imágenes asociadas a una disciplina directamente
    desde la vista de detalle de la disciplina.

    Attributes:
        model (class): Modelo de base del formulario.
        extra (int): Cantidad de formularios vacíos por defecto.
        classes (list): Clases CSS aplicadas al contenedor del inline.
    """
    model = ImagenDisciplina
    extra = 3
    # Se usa 'collapse' por defecto para evitar forzar un scroll excesivo 
    # cuando la disciplina tiene demasiadas imágenes previas cargadas.
    classes = ['collapse']


@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    """
    Configuración administrativa para el modelo Disciplina.

    Attributes:
        list_display (tuple): Campos a presentar como columnas en la lista.
        prepopulated_fields (dict): Reglas para el autocompletado en el formulario.
        inlines (list): Modelos dependientes a gestionar en la misma vista.
    """
    list_display = ('nombre', 'color_hex')
    prepopulated_fields = {'slug': ('nombre',)}
    inlines = [ImagenDisciplinaInline]


@admin.register(Partido)
class PartidoAdmin(admin.ModelAdmin):
    """
    Configuración administrativa para el modelo Partido.

    Attributes:
        list_display (tuple): Columnas de datos visibles en la vista de lista.
        list_filter (tuple): Criterios de filtrado disponibles en el panel lateral.
        date_hierarchy (str): Campo de tipo fecha para permitir navegación temporal superior.
        list_editable (tuple): Atributos a modificar sin entrar al detalle del registro.
        list_select_related (tuple): Relaciones que se consultan vía JOIN en BD.
    """
    list_display = (
        'disciplina', 'rival', 'fecha_hora', 'es_local',
        'resultado_arbolito', 'resultado_rival', 'activo'
    )
    list_filter = ('disciplina', 'es_local', 'activo')
    date_hierarchy = 'fecha_hora'
    
    # Permitir la edición directa desde la cuadrícula facilita la actualización 
    # masiva y rápida de todos los resultados el fin de semana.
    list_editable = ('resultado_arbolito', 'resultado_rival', 'activo')
    
    # Optimización: Se pre-cargan los datos de 'disciplina' mediante JOIN para 
    # evitar el problema de N+1 queries al renderizar las columnas en el list_display.
    list_select_related = ('disciplina',)
