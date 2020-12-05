from django.urls import path
from . import views
urlpatterns = [
    path('', views.index,name='home'),
    path('delete/<city_name>/', views.delete, name='delete'),
    path('about_us/', views.about_us, name='about_us'),
    path('help/', views.help, name='help')
]