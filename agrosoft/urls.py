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
	path('fertilizantes/<int:fertilizante_id>/', views.detalle_fertilizante, name='detallefertilizante'),
	path('fertilizantes/agregar/', views.agregar_fertilizante, name='agregarfertilizante'),
	path('fertilizantes/editar/<int:fertilizante_id>/', views.editar_fertilizante, name='editarfertilizante'),
	path('fertilizantes/eliminar/<int:fertilizante_id>/', views.eliminar_fertilizante, name='eliminarfertilizante'),

	path('personal/', views.listar_personal, name='listarpersonal'),
	path('personal/<int:personal_id>/', views.detalle_personal, name='detallepersonal'),
	path('personal/agregar/', views.agregar_personal, name='agregarpersonal'),
	path('personal/editar/<int:personal_id>/', views.editar_personal, name='editarpersonal'),
	path('personal/eliminar/<int:personal_id>/', views.eliminar_personal, name='eliminarpersonal'),

	path('inventario/', views.listar_bienes, name='listarbienes'),
	path('inventario/<int:inventario_id>/', views.detalle_bien, name='detallebien'),
	path('inventario/agregar/', views.agregar_bien, name='agregarbien'),
	path('inventario/editar/<int:inventario_id>/', views.editar_bien, name='editarbien'),
	path('inventario/eliminar/<int:inventario_id>/', views.eliminar_bien, name='eliminarbien'),
	path('inventario/registrarES/', views.registrares_bien, name='registraresbien'),
	
	
    path('calendario', views.CalendarView.as_view(), name='calendar'),
    path('calendario/evento/new/', views.create_event, name='event_new'),
    path('calendario/evento/edit/<int:pk>/', views.EventEdit.as_view(), name='event_edit'),
    path('calendario/evento/<int:event_id>/details/', views.event_details, name='event-detail'),
	path('calendario/add_eventmember/<int:event_id>', views.add_eventmember, name='add_eventmember'),
    path('calendario/evento/<int:pk>/remove', views.EventMemberDeleteView.as_view(), name="remove_event"),
	path('calendario/eliminar/<int:event_id>', views.eliminar_evento, name="eliminarevento"),

    path('inventario/export1', views.exportBienesCSV, name='export_bienes_csv'),
	path('inventario/export2', views.exportBienesEXCEL, name='export_bienes_excel'),


]