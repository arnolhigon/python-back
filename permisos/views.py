from django.shortcuts import render
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import viewsets
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from .models import Profile, Tarea
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema
from .serializers import *
from rest_framework import status
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from .models import Profile




class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'username' 

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['groups'] = list(user.groups.values_list('name', flat=True)) or ''
        
        try:
            profile = Profile.objects.get(user=user)
            token['proceso'] = profile.proceso
            token['rol'] = profile.rol
        except Profile.DoesNotExist:
            token['proceso'] = 'NA'
            token['rol'] = 'NA'

        return token



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token',
        '/api/token/refresh',
    ]
    return Response(routes)







#permisos para rol prestador, dinamizador
def is_prestador(user):
    return user.groups.filter(name='prestador').exists()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Ya existe un usuario con este nombre.')
        return value

    def validate_password(self, value):
        try:
            user = User(username=self.initial_data.get('username'), email=self.initial_data.get('email'))
            validate_password(value, user=user)
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)



@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response({"message": "Usuario creado exitosamente"}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({"error": "Ya existe un usuario con este nombre."}, status=status.HTTP_400_BAD_REQUEST)
        
    errors = serializer.errors
    error_messages = []
    if 'password' in errors:
        error_messages.extend(errors['password'])
    if 'username' in errors:
        error_messages.extend(errors['username'])
    if error_messages:
        return Response({"error": error_messages}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





from functools import wraps
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required



def group_required(groups):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return JsonResponse({'error': 'Unauthorized'}, status=401)
            
            user_groups = {group.name for group in request.user.groups.all()}
            required_groups = set(groups.split('-'))
            if user_groups.intersection(required_groups):
                return view_func(request, *args, **kwargs)
            else:
                return JsonResponse({'error': 'Forbidden'}, status=403)
        return wrapper
    return decorator



6

from functools import wraps
from django.http import JsonResponse

def group_role_proceso_required(groups=None, rol=None, proceso=None):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return JsonResponse({'error': 'Unauthorized'}, status=401)
            user_groups = {group.name for group in request.user.groups.all()}
            user_profile = request.user.profile

            if groups:
                required_groups = set(groups.split('-'))
                if not user_groups.intersection(required_groups):
                    return JsonResponse({'error': 'Forbidden: Insufficient group permissions'}, status=403)

            if rol and user_profile.rol != rol:
                return JsonResponse({'error': 'Forbidden: Incorrect role'}, status=403)

            if proceso and user_profile.proceso != proceso:
                return JsonResponse({'error': 'Forbidden: Incorrect process'}, status=403)

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator









########################################################################################
@api_view(['GET'])
def profile_list(request):
    profiles = Profile.objects.all()
    serializer = ProfileSerializer(profiles, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])     
def listar_tareas(request):
    if request.method == "GET":
        queryset = Tarea.objects.all()
        serializer = TareasSerializer(queryset, many=True)
        return Response(serializer.data)



@extend_schema(responses=CrearTareaSerializer)
@api_view(['POST',])
@group_role_proceso_required(groups="administrador", rol="NTRL", proceso="GT")
def crear_tarea(request):
    if request.method == "POST":
        serializer = CrearTareaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(responses=TareasSerializer)
@api_view(['PUT'])
def actualizar_tarea(request, id):
    try:
        queryset = Tarea.objects.get(id=id)
    except Tarea.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        serializer = TareasSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def eliminar_tarea(request, id):
    try:
        tarea = Tarea.objects.get(id=id)
    except Tarea.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    tarea.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def tarea(request, id):
    try:
        tarea = Tarea.objects.get(id=id)
        serializer = TareasSerializer(tarea)
        return Response(serializer.data)
    except Tarea.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@extend_schema(responses=ActualizarEstadoSerializer)
@api_view(['PUT'])
def actualizar_estado(request, id):
    try:
        queryset = Tarea.objects.get(id=id)
    except Tarea.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        serializer = ActualizarEstadoSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)