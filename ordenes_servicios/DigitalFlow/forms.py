# DigitalFlow/forms.py

from django import forms
from .models import Orden

class OrdenForm(forms.ModelForm):
    class Meta:
        model = Orden
        fields = '__all__'
        fields = ['identificador', 'empresa', 'responsable', 'problematica', 
                  'servicios_realizados', 'fecha', 'hora_inicio', 'hora_termino', 
                  'nivel_satisfaccion', 'problema_solucionado', 'nombre_encargado', 
                  'nombre_cliente', 'telefono_cliente', 'foto_inicio', 'foto_fin']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time'}),
            'hora_termino': forms.TimeInput(attrs={'type': 'time'}),
        }
