from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import inlineformset_factory, DateInput
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

class InventarioFormulario(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ('nombre', 'descripcion', 'cantidad', 'proveedor', 'fecha_Ingreso', 'fecha_Salida')
    def __init__(self, *args, **kwargs):
        super(InventarioFormulario, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    'class': 'form-control',                    
                }
            )

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        # datetime-local is a HTML5 input type, format to make date time show on fields
        widgets = {
        'fecha_inicio': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        'fecha_fin': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields['fecha_inicio'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['fecha_fin'].input_formats = ('%Y-%m-%dT%H:%M',)            

class AddMemberForm(forms.ModelForm):
  class Meta:
    model = EventMember
    fields = ['user']