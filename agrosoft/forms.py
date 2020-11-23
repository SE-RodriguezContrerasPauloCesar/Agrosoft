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