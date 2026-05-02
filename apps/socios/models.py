"""
Modelos de datos para la aplicación 'socios'.

Se encarga del almacenamiento y validación de las solicitudes
de ingreso de nuevos miembros y del formulario general de contacto.
"""

from django.db import models


class SolicitudSocio(models.Model):
    """
    Entidad temporal que almacena los leads o prospectos enviados desde la web.

    No representa a un Socio confirmado todavía, sino a una persona
    interesada en unirse a la institución.

    Attributes:
        nombre (CharField): Nombre(s) del prospecto.
        apellido (CharField): Apellido(s).
        dni (CharField): Actúa como llave única natural.
        email (EmailField): Obligatorio para facilitar contacto.
        telefono (CharField): Secundario de contacto.
        mensaje (TextField): Espacio libre para dudas.
        estado (CharField): Control burocrático interno de la directiva.
        fecha_solicitud (DateTimeField): Timestamp automático optimizado.
    """
    ESTADOS = (
        ('pendiente', 'Pendiente de contacto'),
        ('contactado', 'Contactado'),
        ('rechazado', 'Rechazado'),
    )

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    
    # Restricción Arquitectónica: El unique=True no solo evita que un mismo usuario cliquee
    # "Enviar" dos veces accidentalmente, sino que protege de ataques de SPAM bots llenando la BD.
    dni = models.CharField(max_length=15, unique=True, help_text="Sin puntos ni espacios")
    
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    mensaje = models.TextField(blank=True, help_text="¿Alguna consulta adicional?")
    
    # Se añade db_index=True ya que seguramente el panel de Admin o código interno
    # empiece a filtrar con mucha regularidad por `estado=pendiente`.
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente', db_index=True)
    
    # El ordering por Meta exige sí o sí un db_index en motores SQL pesados para no atascarse.
    fecha_solicitud = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-fecha_solicitud']
        verbose_name = 'Solicitud de Socio'
        verbose_name_plural = 'Solicitudes de Socios'

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.dni}"
    

class ConsultaContacto(models.Model):
    """
    Libro de quejas, dudas y sugerencias general de la Institución.

    Attributes:
        nombre_usuario (CharField): Firma del emisor.
        email (EmailField): Core param de contacto.
        telefono (CharField): Teléfono opcional.
        mensaje (TextField): Cuerpo primario.
        fecha_envio (DateTimeField): Ordenación temporal.
        leido (BooleanField): Indicador de flujo de trabajo (workflow state).
    """
    nombre_usuario = models.CharField(max_length=150, verbose_name="Nombre o Nro Socio")
    email = models.EmailField()
    telefono = models.CharField(max_length=20, verbose_name="Teléfono", blank=True, null=True)
    mensaje = models.TextField()
    
    # Se procede a indexar fechas y booleanos vitales para control de estado interno.
    fecha_envio = models.DateTimeField(auto_now_add=True, db_index=True)
    leido = models.BooleanField(default=False, db_index=True)

    class Meta:
        verbose_name = "Consulta de Contacto"
        verbose_name_plural = "Consultas de Contacto"
        # Mantenemos el flujo MVT coherente, ordenando de la consulta más nueva a la más vieja
        ordering = ['-fecha_envio']

    def __str__(self):
        # Bug grave de Mantenibilidad resuelto: Originalmente declaraste `def __clstr__(self):`. 
        # Esta "magic function" NO existe nativamente en Python, por lo que nunca se ejecutaba y 
        # los logs/administradores estaban viendo el objeto memoria Django en bruto ("ConsultaContacto Object (1)").
        return f"Consulta de {self.nombre_usuario} - {self.fecha_envio.strftime('%d/%m/%Y')}"
