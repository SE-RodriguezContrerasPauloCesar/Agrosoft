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

# Create your views here.

def home_login(request):
    if request.method == 'POST':
        dni = request.POST.get('dni')
        contra = request.POST.get('contra')
        usuario = authenticate(username = dni, password = contra)
        if usuario is not None:
            if usuario.is_active:
                login(request, usuario)
                if usuario.groups.filter(name='Personal').exists():
                    personal = User.objects.get(username = usuario)
                    return redirect('personal_home', personal.id)
                else:
                    return redirect('admi_home')
        else:
            messages.error(request, 'DNI y/o Contraseña Incorrecto')
            return redirect(reverse('home_login'))
    return render(request, 'home/home_login.html')

def home_logout(request):
    logout(request)
    messages.error(request,'')
    return redirect(reverse('home_login'))

def admi_home(request):
    return render(request, 'admi/admi_home.html')

def personal_home(request, personal_id):
    personal = User.objects.get(pk = personal_id)
    context = {
        'personal': personal,
    }
    return render(request, 'personal/personal_home.html', context)

# Administrador Personal
def admi_agregar_personal(request):
    if request.method == 'POST':
        formulario = PersonalFormulario(request.POST)
        if formulario.is_valid():
            personal = formulario.save()
            grupo = Group.objects.get(name='Personal')
            personal.groups.add(grupo)
            messages.info(request,'Usuario registrado con éxito')
            return redirect(reverse('admi_home'))
    else:
        formulario = PersonalFormulario()
    context = {
        'formulario': formulario
    }
    return render(request, 'admi/admi_agregar_personal.html', context)

# Administrador Listar Personal
def  admi_listar_personal(request):
    personal = User.objects.filter(groups__name='Personal')
    context = {
        'personal': personal,
    }
    return render(request, 'admi/admi_listar_personal.html', context)