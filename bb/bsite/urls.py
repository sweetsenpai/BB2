from django.urls import path
from . import views

urlpatterns = [
    path('loggin', views.logginpage, name='logginpage'),
]
