from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib import messages

from users.models import CustomUser
from urllib.error import HTTPError

import json
import urllib.request


def index(request):
    return render(request, 'index.html')


def get_weather_data(city, units):
    units_item = {
        'celsius': ['metric', '°C', 'meter/sec'],
        'kelvin': ['standard', 'K', 'meter/sec'],
        'fahrenheit': ['imperial', '°F', 'miles/hour'],
    }

    res = urllib.request.urlopen(
        'https://api.openweathermap.org/data/2.5/weather?units=' + units_item[units][0] +
        '&q=' + city + '&appid=6c360926a047ca28830fcab836186bd0').read()
    json_data = json.loads(res)
    data = {
        # all data items you can find on https://openweathermap.org/current
        'cityname': str(json_data['name']),
        'countrycode': str(json_data['sys']['country']),
        'lon': str(json_data['coord']['lon']),
        'lat': str(json_data['coord']['lat']),
        'temp': str(json_data['main']['temp']) + f' {units_item[units][1]}',
        'feels_like': str(json_data['main']['feels_like']) + f' {units_item[units][1]}',
        'wind': str(json_data['wind']['speed']),
        'wind_speed': units_item[units][2],
        'wind_direction': str(json_data['wind']['deg']) + ' deg.',
        'clouds': str(json_data['clouds']['all']) + ' %',
        'pressure': str(json_data['main']['pressure']) + ' hPa',
        'humidity': str(json_data['main']['humidity']) + ' %',

        'icon': str(json_data['weather'][0]['icon']),
    }
    return data


def search_result(request):
    if request.user.is_authenticated:
        user = CustomUser.objects.get(username=request.user.username)
        if len(user.city) == 0:
            if request.method == 'POST':
                city = request.POST['city']
                units = request.POST['flexRadioDefault']
                try:
                    data = get_weather_data(city, units)
                    user.city = city
                    user.units = units
                    user.save()
                except HTTPError:
                    messages.error(request, "Wrong city. Let's try one more time")
                    return redirect('index')
            else:
                messages.info(request, "You don't have a selected city")
                return redirect('index')
        else:
            city = user.city
            units = user.units
            data = get_weather_data(city, units)

    else:
        if request.method == 'POST':
            city = request.POST['city']
            units = request.POST['flexRadioDefault']
            data = get_weather_data(city, units)
        else:
            data = {}
    return render(request, 'result.html', data)



def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if CustomUser.objects.filter(email=email).exists():
                messages.info(request, 'Email already used')
                return redirect('register')
            elif CustomUser.objects.filter(username=username).exists():
                messages.info(request, 'Username already used')
                return redirect('register')
            else:
                user = CustomUser.objects.create_user(username=username, email=email, password=password)
                user.save()
                return render(request, 'login.html', {'username_after_reg': username})
                # return redirect('login')
        else:
            messages.info(request, 'Passwords not the same')
            return render(request, 'register.html', {
                'username_after_reg': username,
                'email_after_reg': email,
            })
            # return redirect('register')
    else:
        return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)

            usery = CustomUser.objects.get(username=username)
            if len(usery.city) == 0:
                messages.info(request, "You don't have a selected city")
                return redirect('index')
            else:
                return redirect('search_result')
        else:
            messages.info(request, 'Credentials invalid')
            return redirect('login')
    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')

def zero_city(request):
    if request.user.is_authenticated:
        user = CustomUser.objects.get(username=request.user.username)
        user.city = ''
        user.save()
    return redirect('/')



def user_page(request):
    if request.user.is_authenticated:
        user = CustomUser.objects.get(username=request.user.username)
        user.city = ''
        user.save()
        return redirect('search_result')
    else:
        return redirect('index')
