from rest_framework import serializers

from car.models import Car

class CarSerializer(serializers.ModelSerializer):

    class Meta: 
        model = Car
        fields = ('id','name', 'color', 'brand')