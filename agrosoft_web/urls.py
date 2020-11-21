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
