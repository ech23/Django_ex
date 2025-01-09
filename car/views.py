from django.shortcuts import render
import logging
# Create your views here.
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.utils.translation import gettext as _
from car.models import Car
from car.serializer import CarSerializer
from django.utils import translation

logger=logging.basicConfig(filename='loginfo.log',format='%(asctime)s - %(levelname)s - %(message)s',level=logging.INFO)
class ListCreateAPIView(generics.ListCreateAPIView):
    model = Car
    serializer_class = CarSerializer
    user_languge = 'es'
    translation.activate(user_languge)
    def get_queryset(self):
        logging.info(_("Fetching all cars"))
        return Car.objects.all()
    
    def create(self, request, *args, **kwargs):
        serializer = CarSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            logging.info(_("Created a new car successfully"))
            return JsonResponse({
                'message': _('Create a new Car successful!')
            }, status=status.HTTP_201_CREATED)
        logging.warning(_("Failed to create a new car with data: %s", request.data))
        return JsonResponse({
            'message': _('Create a new Car unsuccessful!')
        }, status=status.HTTP_400_BAD_REQUEST)

class UpdateDeleteCarView(RetrieveUpdateDestroyAPIView):
    model = Car
    serializer_class = CarSerializer

    def put(self, request, *args, **kwargs):
        logging.debug(_("Updating car with id: %s", kwargs.get('id')))
        car = get_object_or_404(Car, id = kwargs.get('id'))
        serializer = self.get_serializer(car, data = request.data)

        if serializer.is_valid():
            serializer.save()
            logging.info(_("Updated car with id: %s successfully", kwargs.get('id')))
            return JsonResponse(_({'message': 'Update Car successful!'}, status = status.HTTP_200_OK))
        logging.warning(_("Failed to update car with id: %s", kwargs.get('id')))
        return JsonResponse(_({'message':'Update Car unsuccessful!'},status = status.HTTP_400_BAD_REQUEST))
    
    def delete(self, request, *args, **kwargs):
        logging.debug(_("Deleting car with id: %s", kwargs.get('id')))
        car = get_object_or_404(Car, id=kwargs.get('id'))
        serializer = CarSerializer(car, data = request.data)
        if serializer.is_valid():
            serializer.delete()
            logging.info(_("Deleted car with id: %s successfully", kwargs.get('id')))
            return JsonResponse(_({
                'message': 'Delete Car successful!'
            }, status=status.HTTP_200_OK))
        logging.warning(_("Failed to delete car with id: %s", kwargs.get('id')))
        return JsonResponse(_({'message':'Not Found Car!'}, status = status.HTTP_404_NOT_FOUND))
