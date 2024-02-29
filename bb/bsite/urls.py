from django.urls import path
from . import views

urlpatterns = [
    path('loggin', views.logginpage, name='logginpage'),
    path('', views.index_page, name='index_page'),
    path('master', views.master_page, name='master_page')
]
