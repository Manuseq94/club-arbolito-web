"""
Formularios web para la aplicación 'socios'.

Gestiona la lógica de presentación y validación inicial de los datos
ingresados por usuarios anónimos o clientes del club desde el HTML.
"""

from django import forms

from .models import SolicitudSocio


# DRY (Don't Repeat Yourself): Extraemos la inmensa cadena de clases de Tailwind CSS
# a una constante global. Esto evita repetir más de 800 caracteres en el archivo y,
# sobre todo, permite que si mañana el club cambia los bordes de la UI ('rounded-md' a 'rounded-none'),
# el diseñador solo lo tenga que cambiar en esta única variable.
TAILWIND_INPUT_CLASSES = (
    'w-full rounded-md border-gray-300 shadow-sm focus:border-arbolito-verde '
    'focus:ring-arbolito-verde dark:bg-gray-700 dark:border-gray-600 dark:text-white p-2'
)


class SolicitudSocioForm(forms.ModelForm):
    """
    Formulario expuesto al público para la asociación de nuevos miembros.

    Hereda del ModelForm para atarlo a la base de datos, posibilitando
    el guardado automático y la validación nativa (ej: que el email tenga el @).
    """

    class Meta:
        model = SolicitudSocio
        
        # Seguridad Web: Es peligroso habilitar fields = '__all__' en formularios
        # públicos, ya que un atacante podría enviar el campo {estado: 'Aprobado'} 
        # en la petición HTTP saltándose toda la autoridad de la directiva.
        fields = ['nombre', 'apellido', 'dni', 'email', 'telefono', 'mensaje']
        
        widgets = {
            'nombre': forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASSES}),
            'apellido': forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASSES}),
            'dni': forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASSES}),
            'email': forms.EmailInput(attrs={'class': TAILWIND_INPUT_CLASSES}),
            'telefono': forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASSES}),
            # Para Textarea, inyectamos la constante sumando claves extra como 'rows'
            'mensaje': forms.Textarea(attrs={'class': TAILWIND_INPUT_CLASSES, 'rows': 4}),
        }
