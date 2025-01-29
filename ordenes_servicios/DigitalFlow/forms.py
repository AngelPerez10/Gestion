# DigitalFlow/forms.py

from django import forms
from .models import Orden

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
