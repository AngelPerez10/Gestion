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


# Vista para el formulario de usuario
def from_user(request):
    if request.method == 'POST':
        form = OrdenForm(request.POST, request.FILES)
        if form.is_valid():
            orden = form.save(commit=False)

            # Generar el PDF
            buffer = io.BytesIO()
            p = canvas.Canvas(buffer, pagesize=letter)
            p.drawString(100, 750, f"Orden: {orden.identificador}")
            p.drawString(100, 730, f"Empresa: {orden.empresa}")
            p.drawString(100, 710, f"Responsable: {orden.responsable}")
            p.drawString(100, 690, "Firma del Encargado:")
            if orden.firma_encargado:
                p.drawImage(orden.firma_encargado.path, 100, 650, width=150, height=50)
            p.drawString(100, 630, "Firma del Cliente:")
            if orden.firma_cliente:
                p.drawImage(orden.firma_cliente.path, 100, 600, width=150, height=50)
            p.save()

            # Guardar el PDF en la base de datos
            buffer.seek(0)
            pdf_file = ContentFile(buffer.read())
            buffer.close()
            orden.pdf_generado.save(f"orden_{orden.id}.pdf", pdf_file)

            orden.save()
            return redirect('DigitalFlow:listado_ordenes')
    else:
        form = OrdenForm()
    return render(request, 'from_user.html', {'form': form})