from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Masters, Admin
from django.core.exceptions import ObjectDoesNotExist


def index_page(request):
    if request.user.is_superuser:
        return render(request, 'index.html')
    else:
        return redirect('not_authorized')


def not_authorized(request):
    return render(request, 'not_authorized.html')


def master_page(request):
    if request.user.is_superuser or request.user.is_authenticated:
        return render(request, 'master_page.html')
    else:
        return redirect('not_authorized')


def subcat(request):
    return render(request, 'subcat.html')


def masters(request):
    return render(request, 'masters.html')


def images(request):
    return render(request, 'images.html')


def base(request):
    return render(request, 'base.html')


def logginpage(request):
    context = {}
    if request.method == 'POST':
        if request.POST.get('username') is not None and request.POST.get('password') is not None:
            username = request.POST.get('username')
            password = request.POST.get('password')
            try:
                admin = Admin.objects.filter(admin_name=username).filter(admin_password=password).get()
                user = authenticate(username=admin.admin_name, password=admin.admin_password)
                if user is None:
                    User.objects.create_superuser(username=admin.admin_name, password=admin.admin_password)
                login(request, user)
                return redirect('index_page')
            except ObjectDoesNotExist:
                try:
                    master = Masters.objects.filter(name=username).filter(password=password).get()
                    user = authenticate(username=master.name, password=master.password)
                    if user is None:
                        user = User.objects.create_user(username=master.name, password=master.password)
                    login(request, user)
                    return redirect('master_page')

                except ObjectDoesNotExist:
                    messages.success(request, 'Имя пользователя или пароль не найдены!')
    return render(request, 'loggin.html', context)

# TODO ЗАГРУЗКА ДАННЫХ ИЗ БД
# TODO ЛИЧНАЯ СТРАНИЦА

# TODO ХОСТИНГ
# TODO SSL

