from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory
from django.contrib import messages
from django.urls import reverse

# Views de la página web e inicio de sesión.
def home(request):    
    return render(request, 'home/home.html')

def home_historia(request):    
    return render(request, 'home/home_historia.html')

def home_misionvision(request):    
    return render(request, 'home/home_misionvision.html')

def home_productos(request):    
    return render(request, 'home/home_productos.html')

def home_contact(request):    
    return render(request, 'home/home_contact.html')
