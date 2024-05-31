from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__' 



class CrearTareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarea
        fields = ['titulo', 'descripcion',  'estado_actual']


class TareasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarea
        fields = ['id','titulo', 'descripcion', 'created', 'estado_actual']


class ActualizarEstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarea
        fields = ['estado_actual']

