from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm
from django.shortcuts import redirect

from django.views.generic import DeleteView, DetailView
from django.http import HttpResponse
from geoip import geolite2
from geopy import GoogleV3
# from django.utils import simplejson
import json
import datetime
from geopy import GoogleV3
import os


def kharkiv_7(request):

    #Получение имен картинок


    place_image_in_static = os.listdir('weather/static/weatherapp')
    names_images = []
    for name in place_image_in_static:
        name_place_image_in_static = name.split(".")[0]
        print(name_place_image_in_static)
        names_images.append(name_place_image_in_static)
        print('names_images', names_images)


    print('place_image_in_static', place_image_in_static)


    place = 'Everest'

    # Настройка кнопок с местом
    if request.GET.get('place'):
        place = request.GET.get('place')
        print('place по Get параметрам', place)


    # Настройка о получению места
    if request.method == 'POST':
        place = request.POST['place']
        print(place)

    location = GoogleV3(api_key='AIzaSyDi_HeAAJ9AfpJns9PLZdJsfGhOeNx7e9c').geocode(place)

    try:
        lat = str(location.latitude)
        lon = str(location.longitude)
        adres = location.address
        print('Address:', adres)

    #обработка исключений
    except AttributeError as error_message:
        print("Error: geocode failed on input %s with message %s" % (location, error_message))
        adres = ''
        location = 'Miami'
        place = '''Query not found. 
        See the weather in Miami'''
        lat = str(25.7617)
        lon = str(-80.1918)
        print(location)
    real_ip = request.META.get('HTTP_X_REAL_IP')
    print('real_ip', real_ip)





    #Запись координат в локальный JSON файл
    lat_lon = {'lat':lat, 'lon': lon}
    import json
    json_my  = json.dumps(lat_lon)
    print('json_my', json_my)
    with open('data.json', 'w') as outfile:
        json.dump(lat_lon, outfile)













    # Получение данных с openweathermap
    key = "64b63acfeeb28579404f7511a3580c4b"
    url_kharkiv_96 = 'https://api.openweathermap.org/data/2.5/onecall?lat='+ lat + '&lon='+ lon +'&units=metric&exclude=minutely,hourly&appid='+ key
    data_kharkiv_96 = requests.get(url_kharkiv_96).json()
    current_time = datetime.datetime.fromtimestamp(int(data_kharkiv_96 ['current']['dt']))
    today = current_time.strftime('%Y - %m  - %d')
    temp_now = data_kharkiv_96 ['current']['temp']
    icon_now = data_kharkiv_96 ['current']['weather'][0]['icon']
    icon_now_link = 'http://openweathermap.org/img/wn/' + icon_now + '.png'
    date_7 = []
    for i in range (0,8):
        date = datetime.datetime.fromtimestamp(int(data_kharkiv_96['daily'][i]['dt']))
        date  = date.strftime( '%b %d')

        moon_phase = data_kharkiv_96['daily'][i]['moon_phase']
        temp_day = (data_kharkiv_96['daily'][i]['temp']).get('day')
        temp_min = (data_kharkiv_96['daily'][i]['temp']).get('min')
        temp_max = (data_kharkiv_96['daily'][i]['temp']).get('max')
        temp_night = (data_kharkiv_96['daily'][i]['temp']).get('night')
        temp_eve = (data_kharkiv_96['daily'][i]['temp']).get('eve')
        temp_morn = (data_kharkiv_96['daily'][i]['temp']).get('morn')

        temp_day_feels = (data_kharkiv_96['daily'][i]['feels_like']).get('day')
        temp_night_feels = (data_kharkiv_96['daily'][i]['feels_like']).get('night')
        temp_eve_feels = (data_kharkiv_96['daily'][i]['feels_like']).get('eve')
        temp_morn_feels = (data_kharkiv_96['daily'][i]['feels_like']).get('morn')

        pressure = data_kharkiv_96['daily'][i]['pressure']
        dew_point = data_kharkiv_96['daily'][i]['dew_point']
        wind_speed = data_kharkiv_96['daily'][i]['wind_speed']
        wind_gust = data_kharkiv_96['daily'][i]['wind_gust']

        pop = int(100*data_kharkiv_96['daily'][i]['pop'])

        day_week = datetime.datetime.fromtimestamp(int(data_kharkiv_96['daily'][i]['sunrise'])).strftime(" %a ")
        sunrise = datetime.datetime.fromtimestamp(int(data_kharkiv_96['daily'][i]['sunrise'])).strftime(" %a ")

        if 'rain' in data_kharkiv_96['daily'][i]:
            rain = '☂ '+str(data_kharkiv_96['daily'][i]['rain'])+ 'мм'
        else:
            rain = 'no rain'
        print('+', rain)


        icon = data_kharkiv_96['daily'][i]['weather'][0]['icon']
        icon_link = 'http://openweathermap.org/img/wn/' + icon + '.png'


        daily = [date, temp_day, temp_morn, temp_eve, temp_night, temp_min, temp_max,
                 temp_day_feels, temp_morn_feels,temp_eve_feels,  temp_night_feels,
                 moon_phase, icon_link, i, pressure, dew_point, wind_speed, wind_gust, sunrise, pop, day_week, rain]
        date_7.append(daily)


    cont_96 = {'all_data_96': data_kharkiv_96,
               'current_time': datetime.datetime.fromtimestamp(int(data_kharkiv_96 ['current']['dt'])),
               'temp_now': temp_now,
               'moon_phase': moon_phase,
               'temp_feel_now': data_kharkiv_96['current']['feels_like'],
               'date_7': date_7,
               'place': place,
               'adres': adres,
               'lat': lat,
               'lon': lon,
               'json_m': json_my,
               'real_ip': real_ip,
               'place_image_in_static': place_image_in_static,
               'names_images': names_images,
            }

    return render(request, 'weather/kharkiv_7.html', cont_96)


def kharkiv(request):
    key = "64b63acfeeb28579404f7511a3580c4b"
    url_kharkiv = 'https://api.openweathermap.org/data/2.5/weather?q=kharkiv&appid='+ key
    data_kharkiv = requests.get(url_kharkiv).json()

    cont = {'all_data': data_kharkiv,'temp': data_kharkiv['main']['temp'], 'icon': data_kharkiv ['weather'][0] ['icon'],
            'wind_speed' : data_kharkiv['wind']['speed'],
            'wind_direction': data_kharkiv['wind']['deg'],
            'pressure': data_kharkiv['main']['pressure'],
            }
    return render(request, 'weather/kharkiv.html', cont)





def index(request):
    key = "64b63acfeeb28579404f7511a3580c4b"
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + key

    if (request.method ==  'POST'):
        form = CityForm(request.POST)
        form.save()

    #now = datetime.datetime.now()
    #now2 = now.strftime()
    form = CityForm

    cities = City.objects.all()

    all_cities = []

    for city in cities:
        res = requests.get(url.format(city.name)).json()

        city_info = {
            "city": city.name,
            'temp': res['main']['temp'],
            'icon': res['weather'] [0]['icon'],
            #'date': now2

        }
#        print(city_info)

        all_cities.append(city_info)
#        print(all_cities)
    context = {"all_info": all_cities, 'form':  form}
    print(context)

    return  render(request, 'weather/index.html', context )



def Delete(request):
    City.objects.all().delete()
    return redirect('/')



