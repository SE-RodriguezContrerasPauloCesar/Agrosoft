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
    title = 'Lista de convocatorias'
    context = {
		"title": title		
	}
    return render(request, 'agrosoft/lotes/listar_lotes.html', context)




# Views de la Gestión de Usuarios
# Administrador Listar Usuario
def listar_usuario(request):
    usuario = User.objects.filter(groups__name='Administrador')
    context = {
        'usuario': usuario,
    }
    return render(request, 'agrosoft/usuarios/listar_usuarios.html', context)

# Administrador Usuario
def agregar_usuario(request):
    groups = Group.objects.exclude(name='Emprendedor').exclude(name='Mentor')
    
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

#shows user detail
def detalle_usuario(request, usuario_id):
	title = 'Detalle de usuario'
	usuario = User.objects.get(id = usuario_id)

	return render(request, 'agrosoft/usuarios/detalle_usuario.html', locals())

# Administrador Editar Usuario
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
            return redirect('agrosoft:adminhome')
    return render(request, 'agrosoft/usuarios/editar_usuario.html', context)

# Administrador Eliminar Usuario
def eliminar_usuario(request, usuario_id):
    usuario = User.objects.get(id = usuario_id)
    usuario.delete()
    return redirect('agrosoft:adminhome')
