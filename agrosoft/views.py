from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory
from .forms import *
from django.contrib import messages
from django.urls import reverse
from .models import *
from django.db.models import Q

# Views de la página web e inicio de sesión.
# Checks if the user is user or admin type
def system_home(request):	
	if request.user.groups.filter(Q(name='Administrador') | Q(name='Personal')).exists(): 
		return redirect(reverse('agrosoft:adminhome'))
	else:
		return redirect(reverse('agrosoft_accounts:login'))

# Views de la Gestión de Lotes
def listar_lotes(request):
    query_set = Lote.objects.all()
    lotes = reversed(list(query_set))
    context = {
        'lotes': lotes,        
    }
    return render(request, 'agrosoft/lotes/listar_lotes.html', context)   

# Agregar un nuevo Lote
def agregar_lote(request):    
    
    if request.method == 'POST':
        formulario = LoteFormulario(request.POST)
        if formulario.is_valid():            
            lote = formulario.save()                        
            messages.info(request,'Lote registrado con éxito')
            return redirect(reverse('agrosoft:listarlotes'))
    else:
        formulario = LoteFormulario()
    context = {
        'formulario': formulario
    }
    return render(request, 'agrosoft/lotes/agregar_lote.html', context)

# Mostrar detalle de un Lote
def detalle_lote(request, lote_id):
	title = 'Detalle de Lote'
	lote = Lote.objects.get(id = lote_id)

	return render(request, 'agrosoft/lotes/detalle_lote.html', locals())

# Editar un Lote
def editar_lote(request, lote_id):
    lote = Lote.objects.get(id = lote_id)
    if request.method == 'GET':
        form = LoteFormulario(instance = lote)
        context = {
            'form': form
        }
    else:
        form = LoteFormulario(request.POST, instance = lote)
        context = {
            'form': form
        }
        if form.is_valid():
            form.save()
            messages.info(request, 'Lote actualizado')
            return redirect('agrosoft:listarlotes')
    return render(request, 'agrosoft/lotes/editar_lote.html', context)

# Eliminar un Lote registrado
def eliminar_lote(request, lote_id):
    lote = Lote.objects.get(id = lote_id)
    lote.delete()
    messages.info(request, 'Lote eliminado')
    return redirect('agrosoft:listarlotes')

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
    groups = Group.objects.exclude(name='Administrador').exclude(name='Personal')
    
    if request.method == 'POST':
        formulario = UsuarioFormulario(request.POST)
        if formulario.is_valid():
            usuario = formulario.save()
            grupo = Group.objects.get(name='Administrador')
            usuario.groups.add(grupo)
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
    if request.method == 'GET':
        form = CultivoFormulario(instance = cultivo)
        context = {
            'form': form
        }
    else:
        form = CultivoFormulario(request.POST, instance = cultivo)
        context = {
            'form': form
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
    if request.method == 'POST':
        formulario = EnfermedadFormulario(request.POST)
        if formulario.is_valid():
            cultivo = formulario.save()                        
            messages.info(request,'Enfermedad registrada con éxito')
            return redirect(reverse('agrosoft:listarenfermedades'))
    else:
        formulario = EnfermedadFormulario()
    context = {
        'formulario': formulario
    }
    return render(request, 'agrosoft/enfermedades/agregar_enfermedad.html', context)

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