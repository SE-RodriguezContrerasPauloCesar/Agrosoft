from django.urls import include, path
from . import views

app_name = 'agrosoft'

urlpatterns = [     
    path('', views.system_home, name='home'),  
    path('administrador/', views.listar_lotes, name='adminhome'),     

	path('usuario/', views.listar_usuario, name='listarusuarios'),
	path('usuario/<int:usuario_id>/', views.detalle_usuario, name='detalleusuario'),
	path('usuario/agregar/', views.agregar_usuario, name='agregarusuario'),
	path('usuario/editar/<int:usuario_id>/', views.editar_usuario, name='editarusuario'),
	path('usuario/eliminar/<int:usuario_id>/', views.eliminar_usuario, name='eliminarusuario'),

	path('lotes/', views.listar_lotes, name='listarlotes'),
]