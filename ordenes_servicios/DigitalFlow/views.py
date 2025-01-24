from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Orden
from .forms import OrdenForm
from django.contrib import messages
from django.http import HttpResponse
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


# Vista para generar el PDF de una orden
def pdf_orden(request, pk):
    orden = get_object_or_404(Orden, pk=pk)
    
    # Crear la respuesta HTTP con el tipo de contenido de un PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=orden_{orden.identificador}.pdf'
    
    # Crear el objeto canvas para generar el PDF
    p = canvas.Canvas(response, pagesize=letter)
    
    # Agregar contenido al PDF
    p.drawString(100, 750, f"Orden ID: {orden.identificador}")
    p.drawString(100, 730, f"Empresa: {orden.empresa}")
    p.drawString(100, 710, f"Responsable: {orden.responsable}")
    p.drawString(100, 690, f"Problemática: {orden.problematica}")
    p.drawString(100, 670, f"Servicios Realizados: {orden.servicios_realizados}")
    p.drawString(100, 650, f"Fecha: {orden.fecha}")
    p.drawString(100, 630, f"Hora Inicio: {orden.hora_inicio}")
    p.drawString(100, 610, f"Hora Término: {orden.hora_termino}")
    p.drawString(100, 590, f"Nivel de Satisfacción: {orden.nivel_satisfaccion}")
    p.drawString(100, 570, f"Problema Solucionado: {'Sí' if orden.problema_solucionado else 'No'}")
    p.drawString(100, 550, f"Encargado: {orden.nombre_encargado}")
    p.drawString(100, 530, f"Cliente: {orden.nombre_cliente}")
    p.drawString(100, 510, f"Teléfono Cliente: {orden.telefono_cliente}")
    
    # Finalizar el PDF
    p.showPage()
    p.save()
    
    return response


