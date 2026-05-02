"""
Lógica central de presentación para la aplicación 'deportes'.

Este módulo contiene las Vistas (Controllers) que procesan las peticiones URL,
interactúan con los Modelos (Base de Datos) y envían el contexto a las Plantillas.
"""

from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Disciplina, Partido


def disciplina_detalle(request, slug):
    """
    Renderiza la portada central de una disciplina deportiva específica.

    Obtiene la disciplina identificada por su URL (slug), resolviendo sus próximos 
    partidos y sus rendimientos históricos para mostrar en la vista detalle.

    Args:
        request (HttpRequest): Petición actual recibida por el servidor.
        slug (str): Identificador amigable y único del deporte (ej: "futbol-femenino").

    Returns:
        HttpResponse: Renderizado final de `disciplina_detalle.html`.
    """
    # Utilizar API get_object_or_404 es una excelente UX/Seguridad: 
    # En vez de romper el servidor con error 500 si la disciplina no existe,
    # emite automáticamente una página 404 controlada.
    #
    # Optimización 'prefetch_related': Pre-cargamos la relación reversa 'imagenes'  
    # (la galería) para evitar múltiples idas y vueltas a la BD al renderizar el template HTML.
    disciplina = get_object_or_404(
        Disciplina.objects.prefetch_related('imagenes'), 
        slug=slug
    )

    # DRY Extracción Lógica: Separamos el query en una base común en vez de repetirlo 
    # literalmente dos veces para 'proximos_partidos' y 'resultados'.
    #
    # Optimización 'select_related': Adjunta los datos de disciplina al partido via JOIN  
    # para evitar el problema de consultas masivas de (N+1) queries al imprimir los cruces.
    partidos_base = Partido.objects.select_related('disciplina').filter(
        disciplina=disciplina, 
        activo=True
    )

    ahora = timezone.now()

    # Partidos FUTUROS: Filtramos mayores o iguales a la hora de este preciso instante.
    proximos_partidos = partidos_base.filter(fecha_hora__gte=ahora).order_by('fecha_hora')
    
    # Partidos PASADOS (Resultados históricos).
    # Ocurre magia en el ORM: usar slicing de Python `[:3]` no descarga toda la BD 
    # en la RAM para recortarlo, sino que se inyecta directamente como un `LIMIT 3` en SQL.
    resultados_recientes = partidos_base.filter(fecha_hora__lt=ahora).order_by('-fecha_hora')[:3]

    contexto = {
        'disciplina': disciplina,
        'proximos_partidos': proximos_partidos,
        'resultados': resultados_recientes,
    }
    
    return render(request, 'disciplina_detalle.html', contexto)