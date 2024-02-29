from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Masters, Admin
from django.core.exceptions import ObjectDoesNotExist


def index_page(request):
    return render(request, 'index.html')


def logginpage(request):
    context = {}
    if request.method == 'POST':
        if request.POST.get('username') is not None and request.POST.get('password') is not None:
            username = request.POST.get('username')
            password = request.POST.get('password')
            try:
                admin = Admin.objects.filter(admin_name=username).filter(admin_password=password).get()
                user = authenticate(username=admin.name, password=admin.password)
                if user is None:
                    User.objects.create_superuser(username=admin.name, password=admin.password)
                login(request, user)
                return redirect('index_page')
            except ObjectDoesNotExist:
                ...
            try:
                master = Masters.objects.filter(name=username).filter(password=password).get()
                user = authenticate(username=master.name, password=master.password)
                if user is None:
                    user = User.objects.create_user(username=master.name, password=master.password)
                login(request, user)
                return redirect('index_page')

            except ObjectDoesNotExist:
                ...
    return render(request, 'loggin.html', context)


# TODO ПРАВА
# TODO ЗАГРУЗКА ДАННЫХ ИЗ БД
# TODO ЛИЧНАЯ СТРАНИЦА
# TODO ЗАГРУЗКА СООБЩЕНИЙ
# TODO ХОСТИНГ
# TODO SSL

