from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Fertilizante)
admin.site.register(Enfermedad)
admin.site.register(Enfermedad_Fertelizante)
admin.site.register(Trabajador)
admin.site.register(Cultivo)
admin.site.register(Lote)
admin.site.register(Produccion)
admin.site.register(Trabajador_Lote)
admin.site.register(Enfermedad_Lote)
admin.site.register(Inventario)
admin.site.register(Event)
admin.site.register(EventMember)
