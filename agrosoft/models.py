from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.

class Fertilizante(models.Model):
    nombre = models.CharField('Nombre', max_length=200)
    marca = models.CharField('Marca', max_length=200)
    descripcion = models.TextField('Descripción', null=False)
    beneficios = models.TextField('Beneficios', null=False)
    estadoRegistro = models.CharField('Estado de Registros', max_length=2)

class Enfermedad(models.Model):
    nombre = models.CharField('Nombre', max_length=200)
    descripcion = models.TextField('Descripción', null=False)
    estadoRegistro = models.CharField('Estado de Registros', max_length=2)

class Enfermedad_Fertelizante(models.Model):
    fertilizante_id = models.ForeignKey(Fertilizante, on_delete=models.CASCADE)
    enfermedad_id = models.ForeignKey(Enfermedad, on_delete=models.CASCADE)
    dosis = models.TextField('Dosis', null=False)

class Trabajador(models.Model):
    dni = models.IntegerField('DNI', null=False)
    nombre = models.CharField('Nombre', max_length=400)
    apellido = models.CharField('Apellidos', max_length=200)
    fecha_nacimiento = models.DateField('Fecha de Nacimiento', null=False)
    horas_trabajo = models.IntegerField('Horas de Trabajo', null=False)
    genero = models.CharField('Género', max_length=50)
    estadoRegistro = models.CharField('Estado de Registros', max_length=2)

class Cultivo(models.Model):
    nombre = models.CharField('Nombre', max_length=200)
    tipo = models.CharField('Tipo', max_length=200)
    precio = models.FloatField('Precio', null=False)
    estadoRegistro = models.CharField('Estado de Registros', max_length=2)


class Lote(models.Model):
    nombre = models.CharField('Nombre', max_length=200)
    area = models.IntegerField('Área', null=False)
    fecha_riego = models.DateField('Fecha de Riego', null=False)
    produ = models.IntegerField('Produccion', null=False)
    estadoRegistro = models.CharField('Estado de Registros', max_length=2)

class Produccion(models.Model):
    lote_id = models.ForeignKey(Lote, on_delete=models.CASCADE)
    cultivo_id = models.ForeignKey(Cultivo, on_delete=models.CASCADE)
    cajas = models.IntegerField('Cajas', null=False)
    kilogramos = models.IntegerField('KG', null=False)
    total = models.IntegerField('Total', null=False)    

class Trabajador_Lote(models.Model):
    trabajador_id = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    lote_id = models.ForeignKey(Lote, on_delete=models.CASCADE)

class Enfermedad_Lote(models.Model):
    enfermedad_id = models.ForeignKey(Enfermedad, on_delete=models.CASCADE)
    lote_id = models.ForeignKey(Lote, on_delete=models.CASCADE)

class Inventario(models.Model):
    estado_ = (
        ('1','Retirado'),
        ('2','En Inventario')
    )
    nombre = models.CharField('Nombre', max_length=200)
    descripcion = models.TextField('Descripción', null=False)
    cantidad = models.IntegerField('Cantidad', null=False)
    proveedor = models.CharField('Proveedor', max_length=200)
    estado = models.CharField('Estado', choices=estado_, max_length=1)
    encargado = models.CharField('Encargado', max_length=200)
    fecha_Ingreso = models.DateField('Fecha de Ingreso', null=False)
    fecha_Salida = models.DateField('Fecha de Salida', null=False)
    estadoRegistro = models.CharField('Estado de Registros', max_length=2)

class Event(models.Model):    
    titulo = models.CharField(max_length=200, unique=True)
    descripcion = models.TextField()
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
    
    def get_absolute_url(self):
        return reverse('agrosoft:event-detail', args=(self.id,))

    @property
    def get_html_url(self):
        url = reverse('agrosoft:event-detail', args=(self.id,))
        return f'<a class="btn btn-sm btn-primary mb-1" href="{url}"> {self.titulo} </a>'

class EventMember(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['event', 'user']

    def __str__(self):
        return str(self.user)

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.user.username

