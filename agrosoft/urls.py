from django.urls import include, path
from . import views

app_name = 'agrosoft'

urlpatterns = [     
    path('', views.system_home, name='home'),  
    path('administrador/', views.show_lotes, name='adminhome'),     
	path('usuario/', views.listar_usuario, name='userlist'),
	path('usuario/<int:usuario_id>/', views.detalle_usuario, name='userdetail'),
	path('usuario/agregar/', views.agregar_usuario, name='createuser'),
	path('usuario/editar/<int:usuario_id>/', views.editar_usuario, name='edituser'),
	path('usuario/eliminar/<int:usuario_id>/', views.eliminar_usuario, name='deleteuser'),

]