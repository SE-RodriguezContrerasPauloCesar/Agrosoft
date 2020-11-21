"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
from . import models

app_name = 'agrosoft_web'

urlpatterns = [      
    path('', views.home, name='home'),
    path('historia', views.home_historia, name ='home_historia'),    
    path('mision-vision', views.home_misionvision, name='home_misionvision'),
    path('productos', views.home_productos, name='home_productos'),
    path('contactenos', views.home_contact, name = 'home_contact'),    

] 
