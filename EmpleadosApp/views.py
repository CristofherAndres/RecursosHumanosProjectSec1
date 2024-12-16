from django.shortcuts import render
from django.http import JsonResponse

#Importaciones para API
from EmpleadosApp.models import Empleado
from EmpleadosApp.serializers import EmpleadoSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.
def EmpleadosV1(request):
    empleado = {
        'id' : 123,
        'nombre' : 'Juan',
        'apellido' : 'Perez',
        'salario' : 1000,
        'email' : 'juan@perez.cl' 
    }
    return JsonResponse(empleado)

def EmpleadosV2(request):
    empleados = Empleado.objects.all() # SELECT * FROM Empleado
    data = {'empleados': list(empleados.values())}
    return JsonResponse(data)


# GET -> empleadosAPI/ Obtener todos los empleados
# POST -> empleadosAPI/ Crear un empleado

@api_view(['GET','POST'])
def empleado_list(request):
    if request.method == 'GET':
        empleados = Empleado.objects.all()
        serializer = EmpleadoSerializer(empleados, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = EmpleadoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# GET -> empleadosAPI/1/ Obtener un empleado
# PUT -> empleadosAPI/1/ Actualizar un empleado
# DELETE -> empleadosAPI/1/ Eliminar un empleado

@api_view(['GET', 'PUT', 'DELETE'])
def Empleado_detail(request, pk):
    try:
        empleado = Empleado.objects.get(pk=pk)
    except Empleado.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = EmpleadoSerializer(empleado)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        serializer = EmpleadoSerializer(empleado, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        empleado.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)