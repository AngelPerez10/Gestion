# DigitalFlow/forms.py

from django import forms
from .models import Orden

class OrdenForm(forms.ModelForm):
    class Meta:
        model = Orden
        fields = [
            'identificador', 'empresa', 'responsable', 'problematica', 
            'servicios_realizados', 'fecha_inicio', 'hora_inicio', 
            'fecha_finalizacion', 'hora_termino', 'nivel_satisfaccion', 
            'problema_solucionado', 'nombre_encargado', 'nombre_cliente', 
            'telefono_cliente', 'foto_inicio', 'foto_fin', 'firma_encargado', 'firma_cliente'
        ]
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_finalizacion': forms.DateInput(attrs={'type': 'date'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time'}),
            'hora_termino': forms.TimeInput(attrs={'type': 'time'}),
        }
