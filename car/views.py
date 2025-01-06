from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from car.models import Car
from car.serializer import CarSerializer
class ListCreateAPIView(generics.ListCreateAPIView):
    model = Car
    serializer_class = CarSerializer

    def get_queryset(self):
        return Car.objects.all()
    
    def create(self, request, *args, **kwargs):
        serializer = CarSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return JsonResponse({
                'message': 'Create a new Car successful!'
            }, status=status.HTTP_201_CREATED)

        return JsonResponse({
            'message': 'Create a new Car unsuccessful!'
        }, status=status.HTTP_400_BAD_REQUEST)

class UpdateDeleteCarView(RetrieveUpdateDestroyAPIView):
    model = Car
    serializer_class = CarSerializer

    def put(self, request, *args, **kwargs):
        car = get_object_or_404(Car, id = kwargs.get('id'))
        serializer = self.get_serializer(car, data = request.data)

        if serializer.is_valid():
            serializer.save()

            return JsonResponse({'message': 'Update Car successful!'}, status = status.HTTP_200_OK)

        return JsonResponse({'message':'Update Car unsuccessful!'},status = status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        car = get_object_or_404(Car, id=kwargs.get('id'))
        serializer = CarSerializer(data = request.data)
        if serializer.is_valid():
            car.delete()

            return JsonResponse({
                'message': 'Delete Car successful!'
            }, status=status.HTTP_200_OK)
        return JsonResponse({'message':'Not Found Car!'}, status = status.HTTP_404_NOT_FOUND)
