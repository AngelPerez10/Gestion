# DigitalFlow/views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Orden
from .forms import OrdenForm  # Asumiendo que tienes un formulario para la orden

# Vista para mostrar el listado de órdenes
def listado_ordenes(request):
    ordenes = Orden.objects.all()
    return render(request, 'ordenes/listado_ordenes.html', {'ordenes': ordenes})

# Vista para crear una nueva orden
def crear_orden(request):
    if request.method == 'POST':
        form = OrdenForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('DigitalFlow:listado_ordenes')  # Redirige al listado de órdenes
    else:
        form = OrdenForm()
    return render(request, 'ordenes/crear_orden.html', {'form': form})

# Vista para editar una orden existente
def editar_orden(request, pk):
    orden = get_object_or_404(Orden, pk=pk)
    if request.method == 'POST':
        form = OrdenForm(request.POST, instance=orden)
        if form.is_valid():
            form.save()
            return redirect('DigitalFlow:listado_ordenes')  # Redirige al listado de órdenes
    else:
        form = OrdenForm(instance=orden)
    return render(request, 'ordenes/editar_orden.html', {'form': form, 'orden': orden})

# Vista para eliminar una orden
def eliminar_orden(request, pk):
    orden = get_object_or_404(Orden, pk=pk)
    if request.method == 'POST':
        orden.delete()
        return redirect('DigitalFlow:listado_ordenes')  # Redirige al listado de órdenes
    return render(request, 'ordenes/eliminar_orden.html', {'orden': orden})
