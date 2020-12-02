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
	path('lotes/<int:lote_id>/', views.detalle_lote, name='detallelote'),
	path('lotes/agregar/', views.agregar_lote, name='agregarlote'),
	path('lotes/editar/<int:lote_id>/', views.editar_lote, name='editarlote'),
	path('lotes/eliminar/<int:lote_id>/', views.eliminar_lote, name='eliminarlote'),

	path('enfermedades/', views.listar_enfermedad, name='listarenfermedades'),
	path('enfermedad/<int:enfermedad_id>/', views.detalle_enfermedad, name='detalleenfermedad'),
	path('enfermedades/agregar/', views.agregar_enfermedad, name='agregarenfermedad'),
	path('enfermedades/editar/<int:enfermedad_id>/', views.editar_enfermedad, name='editarenfermedad'),
	path('enfermedades/eliminar/<int:enfermedad_id>/', views.eliminar_enfermedad, name='eliminarenfermedad'),

	path('fertilizantes/', views.listar_fertilizante, name='listarfertilizantes'),
]