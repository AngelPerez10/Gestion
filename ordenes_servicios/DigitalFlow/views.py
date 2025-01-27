# Archivo: DigitalFlow/views.py
# Archivo con las vistas de la aplicación DigitalFlow

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Orden
from .forms import OrdenForm
from django.contrib import messages
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
from django.core.files.base import ContentFile
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


# Vista para mostrar el listado de órdenes
def listado_ordenes(request):
    ordenes = Orden.objects.all()
    return render(request, 'ordenes/listado_ordenes.html', {'ordenes': ordenes})


# Vista para crear una nueva orden
def crear_orden(request):
    if request.method == 'POST':
        form = OrdenForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Orden creada exitosamente!')
            return redirect('DigitalFlow:listado_ordenes')  # Redirige al listado de órdenes
        else:
            messages.error(request, 'Hubo un error al crear la orden.')
    else:
        form = OrdenForm()
    return render(request, 'ordenes/crear_orden.html', {'form': form})


# Vista para editar una orden existente
def editar_orden(request, pk):
    orden = get_object_or_404(Orden, pk=pk)
    if request.method == 'POST':
        form = OrdenForm(request.POST, request.FILES, instance=orden)
        if form.is_valid():
            form.save()
            messages.success(request, f'¡La orden {orden.identificador} ha sido editada exitosamente!')
            return redirect('DigitalFlow:listado_ordenes')
        else:
            messages.error(request, 'Hubo un error al editar la orden.')
    else:
        form = OrdenForm(instance=orden)
    return render(request, 'ordenes/editar_orden.html', {'form': form, 'orden': orden})


# Vista para eliminar una orden
def eliminar_orden(request, pk):
    if request.method == 'POST':
        try:
            orden = get_object_or_404(Orden, pk=pk)
            identificador = orden.identificador  # Para mostrarlo en el mensaje
            orden.delete()
            return JsonResponse({'status': 'success', 'message': f'¡La orden {identificador} fue eliminada exitosamente!'}, status=200)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Error al eliminar la orden: {str(e)}'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Método no permitido.'}, status=405)


def from_user(request):
    if request.method == 'POST':
        # Suponiendo que usas un formulario para guardar la orden
        form = OrdenForm(request.POST, request.FILES)
        if form.is_valid():
            nueva_orden = form.save()  # Guarda la orden y devuelve el objeto
            # Redirige a vista_pdf con el ID de la nueva orden
            return redirect('DigitalFlow:vista_pdf', pk=nueva_orden.pk)
    else:
        form = OrdenForm()

    return render(request, 'from_user.html', {'form': form})



def vista_pdf(request, pk):
    orden = get_object_or_404(Orden, pk=pk)
    return render(request, 'vista_pdf.html', {'orden': orden})


