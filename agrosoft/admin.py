from django.contrib import admin
from .models import Fertilizante
from .models import Enfermedad
from .models import Enfermedad_Fertelizante
from .models import Trabajador
from .models import Cultivo
from .models import Lote
from .models import Produccion
from .models import Trabajador_Lote
from .models import Enfermedad_Lote
from .models import Inventario

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
