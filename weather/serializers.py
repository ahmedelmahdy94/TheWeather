from .models import *
from rest_framework import serializers
from django.db.models import Avg
from rest_framework.serializers import (
    EmailField,
    HyperlinkedModelSerializer,
    ModelSerializer,
    ValidationError
    )


class CitySerializer(ModelSerializer):
    # city_name = serializers.CharField(label='City Name')
    class Meta:
        model = City
        fields = "__all__"

    def validate(self, data):
        city = data['name']
        city_qs = City.objects.filter(name=city)
        if city_qs.exists():
            raise ValidationError("This city has already been entered")
        return data

    def create(self, validated_data):
        name = validated_data['name']

        city_obj = City(name = name)
        city_obj.save()
        return validated_data
