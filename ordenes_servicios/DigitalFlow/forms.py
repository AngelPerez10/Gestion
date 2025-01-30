# DigitalFlow/forms.py

from django import forms
from .models import Orden
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistroUsuarioForm(UserCreationForm):
    is_staff = forms.BooleanField(required=False, label="¿Es administrador?", initial=False)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'is_staff']


class OrdenForm(forms.ModelForm):
    class Meta:
        model = Orden
        fields = [
            'identificador', 'empresa', 'responsable', 'nivel_satisfaccion', 
            'nombre_encargado', 'telefono_cliente', 
            'problema_solucionado', 'problematica', 'servicios_realizados', 
            'fecha_inicio', 'hora_inicio', 'fecha_finalizacion', 'hora_termino', 
            'foto_inicio', 'foto_fin'
        ]
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_finalizacion': forms.DateInput(attrs={'type': 'date'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time'}),
            'hora_termino': forms.TimeInput(attrs={'type': 'time'}),
        }
