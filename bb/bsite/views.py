import django.db
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Categories, Subcategories, Masters, Images, Admin
from django.core.exceptions import ObjectDoesNotExist
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect


def index_page(request):
    if not request.user.is_superuser:
        return redirect('not_authorized')

    records = {'cat': Categories.objects.all().order_by('cat_id').values()}
    template = loader.get_template('index.html')

    if request.method == 'POST':
        if request.POST.get('delete_button') is not None:
            try:
                Categories.objects.get(cat_id=request.POST.get('delete_button')).delete()
            except ObjectDoesNotExist:
                ...
        elif request.POST.get('change_button') is not None:
            cat_update = Categories.objects.get(cat_id=request.POST.get('change_button'))
            cat_update.cat_name = request.POST.get('newdata')
            cat_update.save()
        elif request.POST.get('add_button') is not None:
            if request.POST.get('data') != '':
                new_cat = Categories(cat_name=request.POST.get('data'))
                new_cat.save()
        return HttpResponseRedirect('/', request)
    return HttpResponse(template.render(records, request))


def subcat_all(request):
    if not request.user.is_superuser:
        return redirect('not_authorized')

    records = {'sub_cat': Subcategories.objects.all().order_by('sub_id').values()}
    template = loader.get_template('subcat.html')
    if request.method == 'POST':
        if request.POST.get('delete_button') is not None:
            try:
                Subcategories.objects.get(sub_id=request.POST.get('delete_button')).delete()
            except ObjectDoesNotExist:
                ...
        elif request.POST.get('change_button') is not None:
            subcat_update = Subcategories.objects.get(sub_id=request.POST.get('change_button'))
            subcat_update.sub_name = request.POST.get('newdata')
            subcat_update.save()
        return HttpResponseRedirect('subcat', request)
    return HttpResponse(template.render(records, request))


def subcat_dv(request, pk):
    if not request.user.is_superuser:
        return redirect('not_authorized')

    records = {'sub_cat': Subcategories.objects.filter(sub_cat_id=pk).all().values()}
    template = loader.get_template('subcats.html')
    if request.method == 'POST':
        if request.POST.get('delete_button') is not None:
            Subcategories.objects.get(sub_id=request.POST.get('delete_button')).delete()
        elif request.POST.get('change_button') is not None:
            subcat_update = Subcategories.objects.get(sub_id=request.POST.get('change_button'))
            subcat_update.sub_name = request.POST.get('newname')
            print(subcat_update)
            subcat_update.save()
        if request.POST.get('add_button') is not None:
            if request.POST.get('newdata') != '':
                new_subcat = Subcategories(sub_cat=Categories.objects.get(cat_id=pk), sub_name=request.POST.get('newdata'))
                new_subcat.save()
    return HttpResponse(template.render(records, request))


def not_authorized(request):
    return render(request, 'not_authorized.html')


def master_page(request):
    if request.user.is_superuser or request.user.is_authenticated:
        return render(request, 'master_page.html')
    else:
        return redirect('not_authorized')


def masters(request):
    return render(request, 'masters.html')


def images(request):
    return render(request, 'images.html')


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

