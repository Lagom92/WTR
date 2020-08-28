from os import name
from django.contrib import admin
from django.urls import path
from board import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main, name='main'),
    path('choice/', views.choice, name='choice'),
    path('recommend/', views.recommend, name='recommend'),
]
