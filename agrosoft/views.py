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
#here it checks if the user is user or admin type
def system_home(request):
	if request.user.groups.filter(name='Usuario').exists(): 
		return redirect(reverse('agrosoft:usuariohome'))
	if request.user.groups.filter(Q(name='Administrador')).exists(): 
		return redirect(reverse('agrosoft:adminhome'))
	else:
		return redirect(reverse('agrosoft_accounts:login'))


# Views del sistema web - administrador
def admi_home(request):
    return render(request, 'admi/admi_home.html')

def usuario_home(request, usuario_id):
    usuario = User.objects.get(pk = usuario_id)
    context = {
        'usuario': usuario,
    }
    return render(request, 'usuario/usuario_home.html', context)

# Administrador Usuario
def admi_agregar_usuario(request):
    if request.method == 'POST':
        formulario = UsuarioFormulario(request.POST)
        if formulario.is_valid():
            usuario = formulario.save()
            grupo = Group.objects.get(name='Usuario')
            usuario.groups.add(grupo)
            messages.info(request,'Usuario registrado con éxito')
            return redirect(reverse('admi_home'))
    else:
        formulario = UsuarioFormulario()
    context = {
        'formulario': formulario
    }
    return render(request, 'admi/admi_agregar_usuario.html', context)

# Administrador Listar Usuario
def  admi_listar_usuario(request):
    usuario = User.objects.filter(groups__name='Usuario')
    context = {
        'usuario': usuario,
    }
    return render(request, 'admi/admi_listar_usuario.html', context)

# Administrador Eliminar Usuario
def admi_eliminar_usuario(request, usuario_id):
    usuario = User.objects.get(id = usuario_id)
    usuario.delete()
    return redirect('admi_home')

# Administrador Editar Usuario
def admi_editar_usuario(request, usuario_id):
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
            return redirect('admi_home')
    return render(request, 'admi/admi_editar_usuario.html', context)