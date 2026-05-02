"""
Lógica central de presentación para la aplicación 'institucion'.

Agrupa las vistas que alimentan el Home del club (Inicio), 
el catálogo integral de noticias y las páginas de presentación institucionales estáticas.
"""

from datetime import timedelta

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from apps.deportes.models import Partido
from .models import ImagenCarrusel, Multimedia, Noticia


def inicio(request):
    """
    Renderiza la portada (Home) del sitio web del club.

    Inyecta datos cruciales: carrusel activo, panel de noticias destacadas,
    noticias recientes regulares y la agenda de partidos de los próximos 7 días.

    Args:
        request (HttpRequest): Ocurrencia de la petición HTTP.

    Returns:
        HttpResponse: Respuesta compilando la plantilla 'index.html'.
    """
    carrusel = ImagenCarrusel.objects.filter(activo=True).order_by('orden')
    
    # Optimización 'select_related': Al tener que mostrar de qué categoría es cada noticia, 
    # adjuntamos la tabla al query original evitando 8 idas y vueltas al SQL (N+1 Queries).
    # DRY: Definimos este queryset limpio e íntegro como nuestra base transversal.
    noticias_base = Noticia.objects.select_related('categoria').filter(activo=True)
    
    # El slicing [:5] no procesa en Python, intercepta el QuerySet emitiendo "LIMIT 5" en SQL.
    noticias_destacadas = noticias_base.filter(es_destacada=True)[:5]
    noticias_recientes = noticias_base.filter(es_destacada=False)[:3]
    
    ahora = timezone.now()
    fin_semana = ahora + timedelta(days=7)
    
    # Cruce modular (App Deportes): Se adjunta 'disciplina' previniendo nuevamente un cuello N+1.
    proximos_partidos = Partido.objects.select_related('disciplina').filter(
        activo=True, 
        fecha_hora__gte=ahora,
        fecha_hora__lte=fin_semana
    ).order_by('fecha_hora')[:4]

    contexto = {
        'carrusel': carrusel,
        'noticias_destacadas': noticias_destacadas,
        'noticias_recientes': noticias_recientes,
        'proximos_partidos': proximos_partidos,
    }
    
    return render(request, 'index.html', contexto)


def noticia_detalle(request, noticia_id):
    """
    Despliega un artículo periodístico específico o una vista informativa 404 detallada.

    Args:
        request (HttpRequest): Petición actual recibida.
        noticia_id (int): Identificador numérico localizador en Base de Datos.
    """
    # Validamos con select_related desde el minuto uno. get_object_or_404 sigue 
    # siendo imperativo para no escupir errores 500 al cliente si una nota archivada es compartida.
    noticia = get_object_or_404(
        Noticia.objects.select_related('categoria'), 
        id=noticia_id, 
        activo=True
    )
    
    return render(request, 'noticia_detalle.html', {'noticia': noticia})


def noticias_list(request):
    """
    Renderiza el listado histórico completo de noticias con soporte nativo
    para paginación robusta y filtros dinámicos inyectados por URL (Query Params).
    """
    # Nuevamente aseguramos la base de datos trayendo el JOIN de antemano.
    lista_noticias = Noticia.objects.select_related('categoria').filter(
        activo=True
    ).order_by('-fecha_publicacion')
    
    # Captura inteligente y rápida de query strings (?categoria=sociales)
    categoria_filtro = request.GET.get('categoria')
    if categoria_filtro:
        lista_noticias = lista_noticias.filter(categoria__nombre=categoria_filtro)
    
    # Arquitectura de Paginación: El `Paginator` nativo tiene enorme repercusión de Rendimiento.
    # Tras bastidores utiliza los comandos SQL "LIMIT" y "OFFSET" forzando al Servidor 
    # a procesar o descargar estrictamente 6 registros (y no los 500 históricos que existan).
    paginator = Paginator(lista_noticias, 6)
    page_number = request.GET.get('page')
    
    try:
        noticias = paginator.page(page_number)
    except PageNotAnInteger:
        noticias = paginator.page(1)
    except EmptyPage:
        # UX Graceful Degradation: Redirige fluidamente a la última página válida si alteran la URL.
        noticias = paginator.page(paginator.num_pages)

    return render(request, 'noticias_list.html', {'noticias': noticias})


def galeria(request):
    """Renderiza la biblioteca institucional del club (Álbum)."""
    items = Multimedia.objects.all()
    return render(request, 'galeria.html', {'items': items})


# --- Vistas puramente institucionales (Renderizados MVT sin datos inyectados) ---

def historia(request):
    return render(request, 'historia.html')


def sede_social(request):
    return render(request, 'sede_social.html')


def comision_directiva(request):
    return render(request, 'comision_directiva.html')


def terminos_condiciones(request):
    return render(request, 'terminos.html')


def politicas_privacidad(request):
    return render(request, 'privacidad.html')