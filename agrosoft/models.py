from django.db import models

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

