import requests
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm
import datetime

def index(request):
    appid = '55fd3853bd0b725eeba51090dcea85d9'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid='+appid
    v = 'http://api.openweathermap.org/data/2.5/forecast?q={}&&units=metric&appid='+appid
    
    err_msg=''
    message=''
    message_class=''
    if(request.method=='POST'):
        form = CityForm(request.POST)
        if form.is_valid():
            new_city=form.cleaned_data['name']
            existing_city_count=City.objects.filter(name=new_city).count()
            if existing_city_count==0:
                res = requests.get(url.format(new_city)).json()
                if res['cod']==200:
                    form.save()
                else:
                    err_msg='City does not exist in the world!'
            else:
                err_msg='City already exists in the database!'
        if err_msg:
            message=err_msg
            message_class='is-danger'
        else:
            message='City added successfully!'
            message_class='is-success'
    print(err_msg)
    form=CityForm()

    all_cities=[]
    cities=City.objects.all()
    for city in cities:
        res = requests.get(url.format(city.name)).json()

        a = v.format(city)

        full = requests.get(a).json()

        day = datetime.datetime.today()
        today_date = int(day.strftime('%d'))

        forecast_data_list = {} 

        for c in range(0, full['cnt']):
            date_var1 = full['list'][c]['dt_txt']
            date_time_obj1 = datetime.datetime.strptime(date_var1, '%Y-%m-%d %H:%M:%S')
            if int(date_time_obj1.strftime('%d')) == today_date or int(date_time_obj1.strftime('%d')) == today_date+1:
                if int(date_time_obj1.strftime('%d')) == today_date+1:
                    today_date += 1
                forecast_data_list[today_date] = {}
                forecast_data_list[today_date]['date'] = date_time_obj1.strftime('%d %b, %Y')
                forecast_data_list[today_date]['temperature'] = full['list'][c]['main']['temp']
                forecast_data_list[today_date]['icon'] = full['list'][c]['weather'][0]['icon']
                
                today_date += 1
            else:
                pass
        city_info = {
            'city': city.name,
            'temp': res['main']['temp'],
            'icon': res['weather'][0]['icon'],
            'description':res['weather'][0]['description'],
            'humidity': res['main']['humidity'],
            'pressure': res['main']['pressure'],
            'forecast': forecast_data_list,
        }
        all_cities.append(city_info)
    context={
        'all_info':all_cities,
        'form':form,
        'message':message,
        'message_class': message_class
    }

    return render(request, 'weather/index_boot.html', context)

def delete(request, city_name):
        city = City.objects.filter(name = city_name)
        city.delete()
        return redirect('home')

def about_us(request):
    return render(request, 'weather/about_us.html')

def help(request):
    return render(request, 'weather/help.html')