from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('result', views.search_result, name='search_result'),

    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),

    path('zero_city', views.zero_city, name='zero_city'),

    path('user_page', views.user_page, name='user_page'),


]