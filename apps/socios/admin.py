"""
Configuración del panel de administración para la aplicación 'socios'.

Gestiona los formularios de contacto entrantes y las solicitudes
de inscripción de nuevos socios al club.
"""

from django.contrib import admin

from .models import ConsultaContacto, SolicitudSocio


@admin.register(SolicitudSocio)
class SolicitudSocioAdmin(admin.ModelAdmin):
    """
    Configuración administrativa para la entidad SolicitudSocio.

    Attributes:
        list_display (tuple): Columnas visualizadas primarias.
        list_filter (tuple): Filtros laterales derechos por estado y fecha.
        search_fields (tuple): Atributos de texto para la caja de búsqueda web.
        list_editable (tuple): Permite cambiar el estado de manera masiva.
        date_hierarchy (str): Habilita navegación temporal en la base de datos.
    """
    list_display = ('nombre', 'apellido', 'dni', 'fecha_solicitud', 'estado')
    list_filter = ('estado', 'fecha_solicitud')
    search_fields = ('nombre', 'apellido', 'dni', 'email')
    
    # UX/UI Optimización: Facilita a la directiva la rápida aprobación o rechazo  
    # masivo de socios enlistados sin interactuar entrando registro a registro.
    list_editable = ('estado',)
    
    # Feature / Optimización: date_hierarchy añade un paginador horizontal de años/meses/días. 
    # Es extremadamente eficiente a nivel SQL y mejora radicalmente la interfaz nativa.
    date_hierarchy = 'fecha_solicitud'


@admin.register(ConsultaContacto)
class ConsultaContactoAdmin(admin.ModelAdmin):
    """
    Configuración administrativa para los mensajes del formulario de contacto.

    Attributes:
        list_display (tuple): Datos visibles en formato tabla desde la cuadrícula.
        list_filter (tuple): Atributos usados para segmentar lecturas.
        search_fields (tuple): Índice de búsqueda textual integral.
        readonly_fields (tuple): Tupla inmutable de campos de auditoría.
        date_hierarchy (str): Paginador temporal orgánico por fecha de envío.
    """
    list_display = ('nombre_usuario', 'telefono', 'email', 'fecha_envio', 'leido')
    list_filter = ('leido', 'fecha_envio')
    search_fields = ('nombre_usuario', 'email', 'mensaje')
    
    # Concepto Arquitectónico de Inmutabilidad: Se vuelve de 'solo lectura' la fecha 
    # para garantizar que sea un log de auditoría válido. Si a futuro hubiera un reclamo legal 
    # o administrativo, ningún usuario del sistema podría editar cuándo se recibió originalmente la queja.
    readonly_fields = ('fecha_envio',)
    
    date_hierarchy = 'fecha_envio'