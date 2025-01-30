from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import RegistroUsuarioForm
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from .models import Orden
from .forms import OrdenForm
from django.contrib import messages
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt
import os

# Vista de login
def login_view(request):
    if request.user.is_authenticated:
        return redirect('DigitalFlow:listado_ordenes')  # Redirigir si ya está autenticado
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('DigitalFlow:listado_ordenes')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
        else:
            messages.error(request, 'Error al iniciar sesión.')
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})

# Vista para registrar un nuevo usuario
def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)  # No guardar aún en la base de datos
            # Asignar el rol de administrador si 'is_staff' es True
            if form.cleaned_data['is_staff']:
                usuario.is_staff = True
            usuario.save()
            messages.success(request, f'El usuario {usuario.username} ha sido registrado exitosamente.')
            return redirect('DigitalFlow:login')  # Redirige al login después de registrar al usuario
        else:
            messages.error(request, 'Hubo un error al registrar el usuario.')
    else:
        form = RegistroUsuarioForm()

    return render(request, 'registration/register.html', {'form': form})

# Vista para mostrar el listado de órdenes
@login_required
def listado_ordenes(request):
    if not request.user.is_staff:
        return redirect('DigitalFlow:from_user')  # Redirigir a 'from_user' si es un trabajador

    ordenes = Orden.objects.all()
    return render(request, 'ordenes/listado_ordenes.html', {'ordenes': ordenes})

# Vista para crear una nueva orden
@login_required
def crear_orden(request):
    if not request.user.is_staff:
        return redirect('DigitalFlow:from_user')  # Redirigir si es un trabajador

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
@login_required
def editar_orden(request, pk):
    if not request.user.is_staff:
        return redirect('DigitalFlow:from_user')  # Redirigir si es un trabajador

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
@login_required
def eliminar_orden(request, pk):
    if not request.user.is_staff:
        return redirect('DigitalFlow:from_user')  # Redirigir si es un trabajador

    if request.method == 'POST':
        try:
            orden = get_object_or_404(Orden, pk=pk)
            identificador = orden.identificador  # Para mostrarlo en el mensaje
            orden.delete()
            return JsonResponse({'status': 'success', 'message': f'¡La orden {identificador} fue eliminada exitosamente!'}, status=200)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Error al eliminar la orden: {str(e)}'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Método no permitido.'}, status=405)

# Vista 'from_user' para los trabajadores
@login_required
def from_user(request):
    if request.user.is_staff:
        return redirect('DigitalFlow:listado_ordenes')  # Redirigir si es un administrador

    if request.method == 'POST':
        form = OrdenForm(request.POST, request.FILES)
        if form.is_valid():
            nueva_orden = form.save()  # Guarda la orden y devuelve el objeto
            return redirect('DigitalFlow:vista_pdf', pk=nueva_orden.pk)
    else:
        form = OrdenForm()

    return render(request, 'from_user.html', {'form': form})

# Vista para ver el PDF de una orden
@login_required
def vista_pdf(request, pk):
    orden = get_object_or_404(Orden, pk=pk)
    return render(request, 'vista_pdf.html', {'orden': orden})

# Vista para enviar el PDF por correo
@csrf_exempt
def enviar_pdf(request):
    if request.method == "POST":
        try:
            print("Datos recibidos:", request.POST)
            print("Archivos recibidos:", request.FILES)

            pdf_file = request.FILES.get("pdf")
            orden_id = request.POST.get("orden_id")

            if not pdf_file or not orden_id:
                return JsonResponse({"status": "error", "message": "Faltan datos."}, status=400)

            # Configura el correo electrónico
            email = EmailMessage(
                f"Orden de Servicio {orden_id}",
                "Adjunto encontrará la orden de servicio generada.",
                'angeelp7457@gmail.com',  # Aquí puedes poner una dirección genérica o institucional
                ['idolomessi1030@gmail.com', 'aperez74@ucol.mx'],  # Lista de destinatarios
            )


            # Adjuntar el archivo PDF
            email.attach(f"orden_servicio_{orden_id}.pdf", pdf_file.read(), "application/pdf")

            # Enviar el correo
            email.send()

            return JsonResponse({"status": "success", "message": "PDF y fotos enviados correctamente."})

        except Exception as e:
            print("Error:", str(e))
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "error", "message": "Método no permitido."}, status=405)
