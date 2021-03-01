from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.
class Cultivo(models.Model):
    nombre = models.CharField('Nombre', max_length=200)
    tipo = models.CharField('Tipo', max_length=200)
    precio = models.FloatField('Precio', null=False)
    estadoRegistro = models.CharField('Estado de Registros', max_length=2)

class Fertilizante(models.Model):
    nombre = models.CharField('Nombre', max_length=200)
    marca = models.CharField('Marca', max_length=200)
    descripcion = models.TextField('Descripción', null=False)
    beneficios = models.TextField('Beneficios', null=False)
    estadoRegistro = models.CharField('Estado de Registros', max_length=2)

class Enfermedad(models.Model):
    nombre = models.CharField('Nombre', max_length=200)
    descripcion = models.TextField('Descripción', null=False)
    fertilizante = models.ForeignKey(Fertilizante, on_delete=models.CASCADE, null=True)    

class Lote(models.Model):
    fechariego_ = (
        ('Lunes y Miercoles','Lunes y Miercoles'),
        ('Martes y Jueves','Martes y Jueves')
    )
    nombre = models.CharField('Nombre', max_length=50)
    area = models.IntegerField('Área', null=False)
    fecha_riego = models.CharField('Fecha de Riego',  choices=fechariego_,max_length=50)
    produ = models.IntegerField('Produccion', null=True, default="0")
    cultivo = models.ForeignKey(Cultivo, on_delete=models.CASCADE, null=True)
    enfermedad = models.ForeignKey(Enfermedad, on_delete=models.CASCADE, null=True)
    estadoRegistro = models.CharField('Estado de Registro', max_length=2)


class Produccion(models.Model):
    lote = models.ForeignKey(Lote, on_delete=models.CASCADE)
    cultivo = models.ForeignKey(Cultivo, on_delete=models.CASCADE)
    cajas = models.IntegerField('Cajas', null=False)
    kilogramos = models.IntegerField('KG', null=False)
    fecha = models.DateField('Fecha de Registro', null=True, blank=True)	



class Enfermedad_Fertelizante(models.Model):
    fertilizante_id = models.ForeignKey(Fertilizante, on_delete=models.CASCADE)
    enfermedad_id = models.ForeignKey(Enfermedad, on_delete=models.CASCADE)
    dosis = models.TextField('Dosis', null=False)

class Trabajador(models.Model):
    genero_ = (
        ('Masculino','Masculino'),
        ('Femenino','Femenino')
    )
    dni = models.IntegerField('DNI', null=True)
    nombre = models.CharField('Nombre', max_length=400)
    apellido = models.CharField('Apellidos', max_length=200)
    fecha_nacimiento = models.DateField('Fecha de Nacimiento', null=True)
    horas_trabajo = models.IntegerField('Horas de Trabajo', null=True)
    genero = models.CharField('Género',  choices=genero_, max_length=50)
    estadoRegistro = models.CharField('Estado de Registros', max_length=2)
    
class Asistencia(models.Model):
    trabajador_id = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    fecha = models.DateField('Fecha de Asistencia', null=True)
    hora_entrada = models.TimeField('Hora de Entrada', null=True)
    hora_salida = models.TimeField('Hora de Salida', null=True)        

class Trabajador_Lote(models.Model):
    trabajador_id = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    lote_id = models.ForeignKey(Lote, on_delete=models.CASCADE)

class Enfermedad_Lote(models.Model):
    enfermedad_id = models.ForeignKey(Enfermedad, on_delete=models.CASCADE)
    lote_id = models.ForeignKey(Lote, on_delete=models.CASCADE)

class Inventario(models.Model):
    estado_ = (
        ('Retirado','Retirado'),
        ('En Inventario','En Inventario')
    )
    nombre = models.CharField('Nombre', max_length=200)
    descripcion = models.TextField('Descripción', null=False)
    cantidad = models.IntegerField('Cantidad', null=False)
    proveedor = models.CharField('Proveedor', max_length=200)
    estado = models.CharField('Estado', choices=estado_, max_length=20,  null=True)
    encargado = models.CharField('Encargado', max_length=200)
    fecha_Ingreso = models.DateField('Fecha de Ingreso', null=True)
    fecha_Salida = models.DateField('Fecha de Salida', null=True)
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
    lote = models.ForeignKey(Lote, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['event', 'lote']

    def __str__(self):
        return str(self.lote)

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.user.username

