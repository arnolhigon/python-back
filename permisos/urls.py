from django.urls import path
from . import views
from .views import *
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    
 
    path('profile/', views.profile_list),
    path('register/', register_user, name='register_user'),

    path('crear_tarea/', crear_tarea, name='crearTarea'),
    path('listar_tareas/', listar_tareas, name='ListarTareas'),
    path('actualizar_tarea/<int:id>/', actualizar_tarea, name='actualizarTarea'),
    path('eliminar_tarea/<int:id>/', eliminar_tarea, name='eliminarTarea'),
    path('tarea/<int:id>/', tarea, name='Tarea'),
    path('actualizar_estado/<int:id>/', actualizar_estado, name='actualizarEstado'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
