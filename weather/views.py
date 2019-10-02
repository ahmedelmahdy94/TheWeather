import requests
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .forms import  *

from .serializers import  *

from .models import City
from .forms import CityForm


class CityCreateAPIView(CreateAPIView):
    """docstring for UserCreateAPIView."""
    serializer_class = CitySerializer
    queryset = City.objects.all()

class CityAPIView(APIView):

    def get(self,request):
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID=096730b4966a71e66c58c3b0c144c35c'
        cities = City.objects.all()
        weather_data = []
        try:
            for city in cities:
                r = requests.get(url.format(city)).json()

                city_weather = {
                    'city' : city.name,
                    'temperature' : r['main']['temp'],
                    'description' : r['weather'][0]['description'],
                    'icon' : r['weather'][0]['icon'],
                    }

                weather_data.append(city_weather)
        except KeyError:
            pass
        except EXCEPTION as e:
            pass
        print(weather_data)

        return Response(weather_data, status=HTTP_200_OK)


# @login_required (login_url='/login/')
# def index(request):
#     url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID=096730b4966a71e66c58c3b0c144c35c'
#     city = 'Cairo'
#
#     if request.method == 'POST':
#         form = CityForm(request.POST)
#         form.save()
#
#     form = CityForm()
#
#     cities = City.objects.all()
#     weather_data = []
#     try:
#         for city in cities:
#             r = requests.get(url.format(city)).json()
#
#             city_weather = {
#                 'city' : city.name,
#                 'temperature' : r['main']['temp'],
#                 'description' : r['weather'][0]['description'],
#                 'icon' : r['weather'][0]['icon'],
#                 }
#
#             weather_data.append(city_weather)
#     except KeyError:
#         pass
#     except EXCEPTION as e:
#         pass
#     print(weather_data)
#     context = {'weather_data' : weather_data,'user': request.user, 'form' : form}
#     return render(request, 'weather/weather.html', context)
