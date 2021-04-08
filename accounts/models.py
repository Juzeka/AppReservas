from django.db import models
from core.models import Reserva
from django import forms
from django.forms import ModelForm

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ('nome','email','turma','data','horario','quantidade')

        widgets = {
            'nome': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'turma': forms.Select(attrs={'class':'custom-select mr-sm-4'}),
            'data': forms.DateInput(attrs={'type':'date', 'class':'form-control'}),
            'horario': forms.Select(attrs={'class':'custom-select mr-sm-4'}),
            'quantidade': forms.NumberInput(attrs={'class':'custom-select mr-sm-4','min':'0','max':'15'}),
        }