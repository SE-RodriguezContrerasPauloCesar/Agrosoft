from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import inlineformset_factory, DateInput
from django import forms
from .models import *

class UsuarioFormulario(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
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
        fields = ('nombre', 'precio')
    def __init__(self, *args, **kwargs):
        super(CultivoFormulario, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    'class': 'form-control',                    
                }
            )

# Create event form 
class ProduccionForm(forms.ModelForm):
    class Meta:
        model = Produccion
        fields = '__all__'
    # Set required and widgets for fields
    def __init__(self, *args, **kwargs):
        super(ProduccionForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    'class': 'form-control',
                }
            )

    def validate_date(self):
        if date < datetime.date.today():
            raise forms.ValidationError("The date cannot be in the past!")
        return date

class LoteFormulario(forms.ModelForm):
    class Meta:
        model = Lote
        exclude = ('produ','estadoRegistro')
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
        fields = '__all__'
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
        fields = ('nombre', 'apellido', 'genero')
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
        fields = ('nombre', 'descripcion', 'cantidad', 'proveedor')
    def __init__(self, *args, **kwargs):
        super(InventarioFormulario, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    'class': 'form-control',                    
                }
            )

class InventarioSFormulario(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ('encargado', 'fecha_Salida')
    def __init__(self, *args, **kwargs):
        super(InventarioSFormulario, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    'class': 'form-control',                    
                }
            )

class InventarioEFormulario(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ('fecha_Ingreso', )
    def __init__(self, *args, **kwargs):
        super(InventarioEFormulario, self).__init__(*args, **kwargs)
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
    fields = ['lote']