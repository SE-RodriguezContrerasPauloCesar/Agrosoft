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

	path('cultivo/', views.listar_cultivo, name='listarcultivos'),
	path('cultivo/<int:cultivo_id>/', views.detalle_cultivo, name='detallecultivo'),
	path('cultivo/agregar/', views.agregar_cultivo, name='agregarcultivo'),
	path('cultivo/editar/<int:cultivo_id>/', views.editar_cultivo, name='editarcultivo'),
	path('cultivo/eliminar/<int:cultivo_id>/', views.eliminar_cultivo, name='eliminarcultivo'),

	path('lotes/', views.listar_lotes, name='listarlotes'),
]