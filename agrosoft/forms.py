from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from django import forms
from .models import *

class UsuarioFormulario(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')
    def __init__(self, *args, **kwargs):
        super(UsuarioFormulario, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    'class': 'form-control',
                    'pattern': '^((\S+ )*\S+)?$',
                    'title':'No poner espacios en blanco al inicio, al final o seguidos.',
                }
            )

class CultivoFormulario(forms.ModelForm):
    class Meta:
        model = Cultivo
        fields = ('nombre', 'tipo', 'precio')
    def __init__(self, *args, **kwargs):
        super(CultivoFormulario, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    'class': 'form-control',                    
                }
            )

class LoteFormulario(forms.ModelForm):
    class Meta:
        model = Lote
        fields = ('nombre', 'area', 'fecha_riego', 'produ')
    def __init__(self, *args, **kwargs):
        super(LoteFormulario, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    'class': 'form-control',                    
                }
            )

class EnfermedadFormulario(forms.ModelForm):
    class Meta:
        model = Enfermedad
        fields = ('nombre', 'descripcion')
    def __init__(self, *args, **kwargs):
        super(EnfermedadFormulario, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    'class': 'form-control',                    
                }
            )

class FertilizanteFormulario(forms.ModelForm):
    class Meta:
        model = Fertilizante
        fields = ('nombre', 'marca', 'descripcion', 'beneficios')
    def __init__(self, *args, **kwargs):
        super(FertilizanteFormulario, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    'class': 'form-control',                    
                }
            )

class PersonalFormulario(forms.ModelForm):
    class Meta:
        model = Trabajador
        fields = ('dni', 'nombre', 'apellido', 'fecha_nacimiento', 'horas_trabajo', 'genero')
    def __init__(self, *args, **kwargs):
        super(PersonalFormulario, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    'class': 'form-control',                    
                }
            )