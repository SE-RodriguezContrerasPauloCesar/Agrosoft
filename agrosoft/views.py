from datetime import date
from datetime import timedelta
import calendar
from django.utils.safestring import mark_safe
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import Calendar
from django.urls import reverse_lazy
from django.db.models import Sum
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404


from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory
from .forms import *
from django.contrib import messages
from django.urls import reverse
from .models import *
from django.db.models import Q

import csv
import datetime as dt
import xlwt

from .utils import render_to_pdf 
from django.views.generic import View
from django.template.loader import get_template

# Views de la página web e inicio de sesión.
# Checks if the user is user or admin type
def system_home(request):	
	if request.user.groups.filter(Q(name='Administrador') | Q(name='Personal')).exists(): 
		return redirect(reverse('agrosoft:adminhome'))
	else:
		return redirect(reverse('agrosoft_accounts:login'))

# Views de la Gestión de Lotes
# Listar lotes registrados y mostrar información en dashboard
def listar_lotes(request):
    query_set = Lote.objects.all()
    lotes = reversed(list(query_set))

    lotes_count = Lote.objects.count()    
    bienes_count = Inventario.objects.count()    
    personal_count = Trabajador.objects.count()   

    lotes_sorted = Lote.objects.order_by('-produ', 'nombre')    

    menor = min(lotes_sorted,key=lambda x: x.produ)
    mayor = max(lotes_sorted,key=lambda x: x.produ)
    produ_total = Lote.objects.aggregate(Sum('produ'))
    
    #Falta produccion total en soles jalar de gestion de produccion

    context = {
        'lotes': lotes,  
        'bienes_count': bienes_count, 
        'lotes_count': lotes_count,   
        'personal_count': personal_count,
        'lotes_sorted': lotes_sorted,  
        'menor': menor,  
        'mayor': mayor,     
        'produ_total': produ_total,        
    }
    return render(request, 'agrosoft/lotes/listar_lotes.html', context)   

# Agregar un nuevo Lote
def agregar_lote(request):     
    cultivos = Cultivo.objects.all()   
    enfermedades = Enfermedad.objects.all()

    if request.method == 'POST':
        formulario = LoteFormulario(request.POST)
        context = {
			"form": formulario,		
            "cultivos": cultivos,
            "enfermedades": enfermedades
		}
        if formulario.is_valid():            
            lote = formulario.save()                                    
            messages.info(request,'Lote registrado con éxito!')
            return redirect(reverse('agrosoft:listarlotes'))
    else:
        formulario = LoteFormulario()
        context = {
			"form": formulario,            
			"cultivos": cultivos,
            "enfermedades": enfermedades
		}
    context = {
        'formulario': formulario,
        "cultivos": cultivos,
        "enfermedades": enfermedades
    }
    return render(request, 'agrosoft/lotes/agregar_lote.html', locals())

    

# Mostrar detalle de un Lote y Gestionar diferentes aspectos del mismo
def detalle_lote(request, lote_id):
	title = 'Gestión de Lote'
	lote = Lote.objects.get(id = lote_id)    
	return render(request, 'agrosoft/lotes/detalle_lote.html', locals())

# Produccion de un Lote
def produccion_lote(request, lote_id):   
    title = 'Producción de Lote'  
    lote = Lote.objects.get(pk=lote_id)        
    cultivos = Cultivo.objects.all()    
    producciones = Produccion.objects.filter(lote__id=lote_id)
    
    
    caja_total = Produccion.objects.filter(lote__id=lote_id).aggregate(Sum('cajas'))           

    if request.method == 'GET':
        return render(request, 'agrosoft/lotes/produccion_lote.html', locals())   
	
    new_fecha = request.POST.getlist('fecha')	
    assign_to_ids = request.POST.getlist('cultivos')	
    assigned_dates = request.POST.getlist('fecha')	
    cajas = request.POST.getlist('cajas')
	
    kilogramos = request.POST.getlist('kilogramos')
    assigned_cultivos = []

    # Contar cajas totales , este procedimiento sera igual para mostrar en la tabal de lotes la produccion
    
    
    for a in assign_to_ids:	
    	if a == 'Ninguno':	
    		assigned_cultivos.append(a)	
    	else:		        
    		#assigned_cultivos.append(Cultivo.objects.get(id=a))  
            assigned_cultivos.append(Cultivo.objects.get(id=a))
            
            
    d=0
    for t, af, b ,c in zip(new_fecha, assigned_dates, cajas, kilogramos):
        if t == '' and assigned_cultivos[c] == 'Ninguno' and b == '' and c == '':
			
            return redirect(reverse('agrosoft:produlote', kwargs={'lote_id':lote_id}))
        else:					
            if assigned_cultivos[d] == 'Ninguno':				
                if af == '':									
                    task = Produccion(fecha=af, lote=lote)
                else:
                    task =Produccion(fecha=af, lote=lote, cajas=b, kilogramos=c)			
            else:
				
                if af == '':
					
                    task = Produccion(fecha=af, lote=lote, cultivo=assigned_cultivos[d])
				
                else:
					
                   
                    task = Produccion(fecha=af, lote=lote, cultivo=assigned_cultivos[d], cajas=b, kilogramos=c)                   		
			
            d = d+1
			
            task.save()	
            
    d = 0
		     
    return redirect(reverse('agrosoft:produlote', kwargs={'lote_id':lote_id}))
		

  

# Editar un Lote
def editar_lote(request, lote_id):
    lote = Lote.objects.get(id = lote_id)    
    cultivos = Cultivo.objects.all()   
    enfermedades = Enfermedad.objects.all()    
    lote_produ = lote.produ
    
    if request.method == 'GET':
        form = LoteFormulario(instance = lote)
        context = {
            'form': form,
            "cultivos": cultivos,
            "enfermedades": enfermedades,
            "lote_produ": lote_produ,

        }
    else:
        form = LoteFormulario(request.POST, instance = lote)
        context = {
            'form': form,
            "cultivos": cultivos,
            "enfermedades": enfermedades,
            "lote_produ": lote_produ,
        }
        if form.is_valid():
            form.save()
            messages.info(request, 'Lote actualizado con éxito!')
            return redirect('agrosoft:listarlotes')
    return render(request, 'agrosoft/lotes/editar_lote.html', context)

# Eliminar un Lote registrado
def eliminar_lote(request, lote_id):
    lote = Lote.objects.get(id = lote_id)
    lote.delete()
    messages.info(request, 'Lote eliminado con éxito!')
    return redirect('agrosoft:listarlotes')


# Views de la Gestión de Producción

# Eliminar un Produccion registrado
def eliminar_produccion(request, lote_id, produccion_id):    
	task = get_object_or_404(Produccion, pk=produccion_id)
	task.delete()

	return redirect(reverse('agrosoft:produlote', kwargs={'lote_id':lote_id}))


# Views de la Gestión de Usuarios
# Listar Usuarios registrados
def listar_usuario(request):
    usuario = User.objects.filter(groups__name='Administrador')
    context = {
        'usuario': usuario,
    }
    return render(request, 'agrosoft/usuarios/listar_usuarios.html', context)

# Agregar un nuevo Usuario
def agregar_usuario(request):
    group = Group.objects.get(name='Administrador')     

    if request.method == 'POST':
        formulario = UsuarioFormulario(request.POST)
        if formulario.is_valid():
            usuario = formulario.save()
            group = Group.objects.get(name='Administrador')
            usuario.groups.add(group)
            messages.info(request,'Usuario registrado con éxito')
            return redirect(reverse('agrosoft:listarusuarios'))
    else:
        formulario = UsuarioFormulario()
    context = {
        'formulario': formulario
    }
    return render(request, 'agrosoft/usuarios/agregar_usuario.html', context)

# Mostrar detalle de un usuario
def detalle_usuario(request, usuario_id):
	title = 'Detalle de usuario'
	usuario = User.objects.get(id = usuario_id)

	return render(request, 'agrosoft/usuarios/detalle_usuario.html', locals())

# Editar un Usuario
def editar_usuario(request, usuario_id):
    usuario = User.objects.get(id = usuario_id)
    if request.method == 'GET':
        form = UsuarioFormulario(instance = usuario)
        context = {
            'form': form
        }
    else:
        form = UsuarioFormulario(request.POST, instance = usuario)
        context = {
            'form': form
        }
        if form.is_valid():
            form.save()
            messages.info(request, 'Usuario actualizado')
            return redirect('agrosoft:listarusuarios')
    return render(request, 'agrosoft/usuarios/editar_usuario.html', context)

# Eliminar un Usuario registrado
def eliminar_usuario(request, usuario_id):
    usuario = User.objects.get(id = usuario_id)
    usuario.delete()
    messages.info(request, 'Usuario eliminado con éxito')
    return redirect('agrosoft:listarusuarios')

# Views de la Gestión de Cultivos
# Listar Cultivos registrados
def listar_cultivo(request):
    query_set = Cultivo.objects.all()
    cultivos = reversed(list(query_set))
    context = {
        'cultivos': cultivos,        
    }
    return render(request, 'agrosoft/cultivos/listar_cultivos.html', context)      

# Agregar un nuevo Cultivo
def agregar_cultivo(request):    
    
    if request.method == 'POST':
        formulario = CultivoFormulario(request.POST)
        if formulario.is_valid():
            cultivo = formulario.save()                        
            messages.info(request,'Cultivo registrado con éxito')
            return redirect(reverse('agrosoft:listarcultivos'))
    else:
        formulario = CultivoFormulario()
    context = {
        'formulario': formulario
    }
    return render(request, 'agrosoft/cultivos/agregar_cultivo.html', context)

# Mostrar detalle de un cultivo
def detalle_cultivo(request, cultivo_id):
	title = 'Detalle de Cultivo'
	cultivo = Cultivo.objects.get(id = cultivo_id)

	return render(request, 'agrosoft/cultivos/detalle_cultivo.html', locals())

# Editar un Cultivo
def editar_cultivo(request, cultivo_id):
    cultivo = Cultivo.objects.get(id = cultivo_id)
    fertilizantes = Fertilizante.objects.all()    
    if request.method == 'GET':
        form = CultivoFormulario(instance = cultivo)
        context = {
            'form': form,
            "fertilizantes": fertilizantes,
        }
    else:
        form = CultivoFormulario(request.POST, instance = cultivo)
        context = {
            'form': form,
            "fertilizantes": fertilizantes,
        }
        if form.is_valid():
            form.save()
            messages.info(request, 'Cultivo actualizado')
            return redirect('agrosoft:listarcultivos')
    return render(request, 'agrosoft/cultivos/editar_cultivo.html', context)


# Eliminar un Cultivo registrado
def eliminar_cultivo(request, cultivo_id):
    cultivo = Cultivo.objects.get(id = cultivo_id)
    cultivo.delete()
    messages.info(request, 'Cultivo eliminado')
    return redirect('agrosoft:listarcultivos')

# Views de la Gestion de Enfermedad
# Listar Enfermedades Registradas
def listar_enfermedad(request):
    query_set = Enfermedad.objects.all()
    enfermedades = reversed(list(query_set))
    context = {
        'enfermedades': enfermedades,        
    }
    return render(request, 'agrosoft/enfermedades/listar_enfermedades.html', context)

# Agregar nueva Enfermedad
def agregar_enfermedad(request):
    fertilizantes = Fertilizante.objects.all()   
    if request.method == 'POST':
        formulario = EnfermedadFormulario(request.POST)
        context = {
			"formulario": formulario,		
            "fertilizantes": fertilizantes,            
		}
        if formulario.is_valid():
            enfermedad = formulario.save()                        
            messages.info(request,'Enfermedad registrada con éxito')
            return redirect(reverse('agrosoft:listarenfermedades'))
    else:
        formulario = EnfermedadFormulario()
        context = {
			"formulario": formulario,		
            "fertilizantes": fertilizantes,            
		}
    context = {
        'formulario': formulario,
        'fertilizantes': fertilizantes
    }
    return render(request, 'agrosoft/enfermedades/agregar_enfermedad.html', locals())


# Editar un Enfermedad
def editar_enfermedad(request, enfermedad_id):
    enfermedad = Enfermedad.objects.get(id = enfermedad_id)
    if request.method == 'GET':
        form = EnfermedadFormulario(instance = enfermedad)
        context = {
            'form': form
        }
    else:
        form = EnfermedadFormulario(request.POST, instance = enfermedad)
        context = {
            'form': form
        }
        if form.is_valid():
            form.save()
            messages.info(request, 'Enfermedad actualizada')
            return redirect('agrosoft:listarenfermedades')
    return render(request, 'agrosoft/enfermedades/editar_enfermedad.html', context)

# Mostrar detalle de Enfermedad
def detalle_enfermedad(request, enfermedad_id):
	title = 'Detalle de Enfermedad'
	enfermedad = Enfermedad.objects.get(id = enfermedad_id)

	return render(request, 'agrosoft/enfermedades/detalle_enfermedad.html', locals())

# Eliminar un Enfermedad registrada
def eliminar_enfermedad(request, enfermedad_id):
    enfermedad = Enfermedad.objects.get(id = enfermedad_id)
    enfermedad.delete()
    messages.info(request, 'Enfermedad eliminada')
    return redirect('agrosoft:listarenfermedades')

# Views de la Gestion de Fertilizante
# Listar Fertilizantes Registradas
def listar_fertilizante(request):
    query_set = Fertilizante.objects.all()
    fertilizantes = reversed(list(query_set))
    context = {
        'fertilizantes': fertilizantes,        
    }
    return render(request, 'agrosoft/fertilizantes/listar_fertilizantes.html', context)

# Agregar nuevo Fertilizante
def agregar_fertilizante(request):
    if request.method == 'POST':
        formulario = FertilizanteFormulario(request.POST)
        if formulario.is_valid():
            cultivo = formulario.save()                        
            messages.info(request,'Fertilizante registrado con éxito')
            return redirect(reverse('agrosoft:listarfertilizantes'))
    else:
        formulario = FertilizanteFormulario()
    context = {
        'formulario': formulario
    }
    return render(request, 'agrosoft/fertilizantes/agregar_fertilizante.html', context)

# Mostrar detalle de Fertilizante
def detalle_fertilizante(request, fertilizante_id):
	title = 'Detalle de Fertilizante'
	fertilizante = Fertilizante.objects.get(id = fertilizante_id)

	return render(request, 'agrosoft/fertilizantes/detalle_fertilizante.html', locals())

# Eliminar Fertilizante registrado
def eliminar_fertilizante(request, fertilizante_id):
    fertilizante = Fertilizante.objects.get(id = fertilizante_id)
    fertilizante.delete()
    messages.info(request, 'Fertilizante eliminado')
    return redirect('agrosoft:listarfertilizantes')

# Editar Fertilizante
def editar_fertilizante(request, fertilizante_id):
    fertilizante = Fertilizante.objects.get(id = fertilizante_id)
    if request.method == 'GET':
        form = FertilizanteFormulario(instance = fertilizante)
        context = {
            'form': form
        }
    else:
        form = FertilizanteFormulario(request.POST, instance = fertilizante)
        context = {
            'form': form
        }
        if form.is_valid():
            form.save()
            messages.info(request, 'Fertilizante actualizado')
            return redirect('agrosoft:listarfertilizantes')
    return render(request, 'agrosoft/fertilizantes/editar_fertilizante.html', context)

# Views de la Gestion de Personal
# Listar personal Registradas
def listar_personal(request):
    query_set = Trabajador.objects.all()
    personal = reversed(list(query_set))
    context = {
        'personal': personal,
    }
    return render(request, 'agrosoft/personal/listar_personal.html', context)

# Agregar nuevo Personal
def agregar_personal(request):
    if request.method == 'POST':
        formulario = PersonalFormulario(request.POST)
        if formulario.is_valid():
            personal = formulario.save()                        
            messages.info(request,'Personal registrado con éxito')
            return redirect(reverse('agrosoft:listarpersonal'))
    else:
        formulario = PersonalFormulario()
    context = {
        'formulario': formulario
    }
    return render(request, 'agrosoft/personal/agregar_personal.html', context)

# Eliminar personal registrado
def eliminar_personal(request, personal_id):
    personal = Trabajador.objects.get(id = personal_id)
    personal.delete()
    messages.info(request, 'Personal eliminado')
    return redirect('agrosoft:listarpersonal')

# Mostrar detalle de Personal
def detalle_personal(request, personal_id):
	title = 'Detalle de Personal'
	personal = Trabajador.objects.get(id = personal_id)
	return render(request, 'agrosoft/personal/detalle_personal.html', locals())

# Editar Personal
def editar_personal(request, personal_id):
    personal = Trabajador.objects.get(id = personal_id)
    if request.method == 'GET':
        form = PersonalFormulario(instance = personal)
        context = {
            'form': form
        }
    else:
        form = PersonalFormulario(request.POST, instance = personal)
        context = {
            'form': form
        }
        if form.is_valid():
            form.save()
            messages.info(request, 'Personal actualizado')
            return redirect('agrosoft:listarpersonal')
    return render(request, 'agrosoft/personal/editar_personal.html', context)

# Mostrar detalle de Personal
def registro_asistencia(request):
	title = 'Registro de Asistencia de Personal'
	
	return render(request, 'agrosoft/personal/registro_asistencia.html', locals())

# Mostrar detalle de Personal
def historial_asistencia(request):
	title = 'Detalle de Personal'
	
	return render(request, 'agrosoft/personal/historial_asistencia.html', locals())

# Views de la Gestión de Inventario
# Listar Bienes registrados
def listar_bienes(request):
    query_set = Inventario.objects.all()
    bienes = reversed(list(query_set))
    context = {
        'bienes': bienes,        
    }
    return render(request, 'agrosoft/inventario/listar_bienes.html', context)      

# Agregar un nuevo Bien
def agregar_bien(request):    
    
    if request.method == 'POST':
        formulario = InventarioFormulario(request.POST)
        if formulario.is_valid():
            bien = formulario.save()                        
            messages.info(request,'Bien registrado con éxito')
            return redirect(reverse('agrosoft:listarbienes'))
    else:
        formulario = InventarioFormulario()
    context = {
        'formulario': formulario
    }
    return render(request, 'agrosoft/inventario/agregar_bien.html', context)

# Mostrar detalle de un Bien
def detalle_bien(request, inventario_id):
	title = 'Detalle de Bien'
	bien = Inventario.objects.get(id = inventario_id)

	return render(request, 'agrosoft/inventario/detalle_bien.html', locals())

# Editar un Bien
def editar_bien(request, inventario_id):
    bien = Inventario.objects.get(id = inventario_id)
    if request.method == 'GET':
        form = InventarioFormulario(instance = bien)
        context = {
            'form': form
        }
    else:
        form = InventarioFormulario(request.POST, instance = bien)
        context = {
            'form': form
        }
        if form.is_valid():
            form.save()
            messages.info(request, 'Bien actualizado')
            return redirect('agrosoft:listarbienes')
    return render(request, 'agrosoft/inventario/editar_bien.html', context)

# Eliminar un Bien registrado
def eliminar_bien(request, inventario_id):
    bien = Inventario.objects.get(id = inventario_id)
    bien.delete()
    messages.info(request, 'Bien eliminado')
    return redirect('agrosoft:listarbienes')

# Registrar la E/S de un Bien
def registrares_bien(request, inventario_id):    
    bien = Inventario.objects.get(id = inventario_id)
    return render(request, 'agrosoft/inventario/registroES_bien.html', locals())
	
# Editar un Bien
def registrare_bien(request, inventario_id):
    bien = Inventario.objects.get(id = inventario_id)
    bien.estado= '2'
    bien.encargado=""
    bien.save()
    if request.method == 'POST':
        formulario = InventarioEFormulario(request.POST,instance = bien)
        if formulario.is_valid():
            bien = formulario.save()                        
            messages.info(request,'Bien registrado con éxito')
            return redirect(reverse('agrosoft:listarbienes'))
    else:
        formulario = InventarioEFormulario(instance = bien)
    context = {
        'formulario': formulario
    }
    return render(request, 'agrosoft/inventario/registroE.html', context)
    

    # Editar un Bien
def registrars_bien(request, inventario_id):    
    bien = Inventario.objects.get(id = inventario_id)
    bien.estado= '1'
    bien.save()
    if request.method == 'POST':
        formulario = InventarioSFormulario(request.POST,instance = bien)
        if formulario.is_valid():
            bien = formulario.save()                        
            messages.info(request,'Bien registrado con éxito')
            return redirect(reverse('agrosoft:listarbienes'))
    else:
        formulario = InventarioSFormulario(instance = bien)
    context = {
        'formulario': formulario
    }
    return render(request, 'agrosoft/inventario/registroS.html', context)
    

# Views de la Gestion de Calendario
# Obtener información necesaria para el calendario
def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return dt.date.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month
    
# Mostrar la información del calendario
class CalendarView(LoginRequiredMixin, generic.ListView):
    login_url = 'signup'
    model = Event
    template_name = 'agrosoft/calendario/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

# Crear un evento para una determinada fecha
def create_event(request):    
    form = EventForm(request.POST or None)
    if request.POST and form.is_valid():
        titulo = form.cleaned_data['titulo']
        descripcion = form.cleaned_data['descripcion']
        fecha_inicio = form.cleaned_data['fecha_inicio']
        fecha_fin = form.cleaned_data['fecha_fin']
        Event.objects.get_or_create(            
            titulo=titulo,
            descripcion=descripcion,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )
        return HttpResponseRedirect(reverse('agrosoft:calendar'))
    return render(request, 'agrosoft/calendario/event.html', {'form': form})

# Eliminar un evento registrado 
def eliminar_evento(request, event_id):
    event = Event.objects.get(id = event_id)
    event.delete()
    messages.info(request, 'Evento eliminado')
    return redirect('agrosoft:calendar')

# Editar un evento para una determinada fecha
class EventEdit(generic.UpdateView):
    model = Event
    fields = ['titulo', 'descripcion', 'fecha_inicio', 'fecha_fin']
    template_name = 'agrosoft/calendario/event.html'

# Ver los detalles de un evento para una determinada fecha
def event_details(request, event_id):
    event = Event.objects.get(id=event_id)
    eventmember = EventMember.objects.filter(event=event)
    context = {
        'event': event,
        'eventmember': eventmember
    }
    return render(request, 'agrosoft/calendario/event-details.html', context)

# Añadir un usuario registrado a un determinado evento
def add_eventmember(request, event_id):
    forms = AddMemberForm()
    lotes = Lote.objects.all()
    if request.method == 'POST':
        forms = AddMemberForm(request.POST)
        if forms.is_valid():
            member = EventMember.objects.filter(event=event_id)
            event = Event.objects.get(id=event_id)
            if member.count() <= 9:
                lote = forms.cleaned_data['lote']
                EventMember.objects.create(
                    event=event,
                    lote=lote
                )
                return redirect('agrosoft:calendar')
                
            else:
                print('--------------User limit exceed!-----------------')
    context = {
        'form': forms,
        'lotes': lotes
    }
    return render(request, 'agrosoft/calendario/add_member.html', context)

# Eliminar un usuario registrado a un determinado evento
class EventMemberDeleteView(generic.DeleteView):
    model = EventMember
    template_name = 'agrosoft/calendario/event_delete.html'
    success_url = reverse_lazy('agrosoft:calendar')

# GESTIÓN DE REPORTES
# Reportes de bienes de la empresa
def exportBienesCSV(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment; filename=BienesAGROSERVIC_'+ str(dt.date.today())+'.csv'
    writer = csv.writer(response)
    writer.writerow(['Nombre','Descripcion','Cantidad','Proveedor','Fecha Ingreso','Fecha Salida'])
    query_set = Inventario.objects.all()
    bienes = reversed(list(query_set))    
    for bien in bienes:
        writer.writerow([bien.nombre,bien.descripcion,bien.cantidad,bien.proveedor,bien.fecha_Ingreso,bien.fecha_Salida])
   
    return response

def exportBienesEXCEL(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition']='attachment; filename=BienesAGROSERVIC_'+ str(dt.date.today())+'.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Bienes')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Nombre','Descripcion','Cantidad','Proveedor','Fecha Ingreso','Fecha Salida']   

    for col_num in range(len(columns)):
        ws.write(row_num,col_num,columns[col_num],font_style)
    font_style = xlwt.XFStyle()

    rows = Inventario.objects.values_list('nombre','descripcion','cantidad','proveedor','fecha_Ingreso','fecha_Salida')
    
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
             ws.write(row_num,col_num,str(row[col_num]),font_style)

    wb.save(response)

    return response

class GeneratePDF(View):
    def get(self, request, *args, **kwargs):
        template = get_template('agrosoft/inventario/pdf-output.html')
        context = {
            "invoice_id": 123,
            "customer_name": "John Cooper",
            "amount": 1399.99,
            "today": "Today",
        }
        html = template.render(context)
        pdf = render_to_pdf('agrosoft/inventario/pdf-output.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')            
            filename = "BienesAgroservic_%s.pdf" %(str(dt.date.today()))
            content = "inline; filename=%s" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename=%s" %(filename)
            response['Content-Disposition'] = content
            return response
            
        return HttpResponse("Not found")

