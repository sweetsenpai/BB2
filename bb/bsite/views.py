import django.db
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Categories, Subcategories, Masters, Images, Admin
from django.core.exceptions import ObjectDoesNotExist
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
import secrets
import string


def create_password():
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(10))
    return password


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
        elif request.POST.get('add_button') is not None:
            if request.POST.get('newdata') != '':
                new_subcat = Subcategories(sub_cat=Categories.objects.get(cat_id=pk), sub_name=request.POST.get('newdata'))
                new_subcat.save()
    return HttpResponse(template.render(records, request))


def masters(request):
    records = {'masters': Masters.objects.prefetch_related().order_by('-master_id')}
    template = loader.get_template('masters.html')
    if request.method == 'POST':
        if request.POST.get('delete_button') is not None:
            Masters.objects.get(master_id=request.POST.get('delete_button')).delete()
        if request.POST.get('change_button') is not None:

            if not request.POST.getlist('visability'):
                visability = False
            else:
                visability = True
            master = Masters.objects.get(master_id=request.POST.get('change_button'))
            print(master)
            master.visability = visability
            master.save()

    return HttpResponse(template.render(records, request))


def masters_dv(request, pk):
    if not request.user.is_superuser:
        return redirect('not_authorized')

    records = {'masters': Masters.objects.filter(sub_master=pk).all().values().order_by('-master_id')}
    template = loader.get_template('master.html')
    if request.method == 'POST':
        if request.POST.get('delete_button') is not None:
            try:
                master = Masters.objects.get(master_id=request.POST.get('delete_button'))
                master.sub_master.clear()

            except ObjectDoesNotExist:
                ...
        if request.POST.get('add_button') is not None:
            if request.POST.get('newdata') != '':
                new_subcat = Masters(name=request.POST.get('newdata'), password=create_password())
                sub = Subcategories.objects.get(sub_id=pk)
                new_subcat.save()
                new_subcat.sub_master.add(sub)
                new_subcat.save()
        if request.POST.get('change_button') is not None:
            if not request.POST.getlist('visability'):
                visability = False
            else:
                visability = True
            master = Masters.objects.get(master_id=request.POST.get('change_button'))
            print(master)
            master.visability = visability
            master.save()
    return HttpResponse(template.render(records, request))


def master_page(request, pk):
    if not request.user.is_superuser or not request.user.is_authenticated:
        return redirect('not_authorized')
    records = {'masters': [Masters.objects.get(master_id=pk)]}
    print(records['masters'])
    template = loader.get_template('master_page.html')
    return HttpResponse(template.render(records, request))


def settings(request, pk):
    return render(request, 'images.html')


def images(request, pk):
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


def not_authorized(request):
    return render(request, 'not_authorized.html')


# TODO ЛИЧНАЯ СТРАНИЦА
# TODO ЗАГРУЗКА ПИКЧ
# TODO ХОСТИНГ
# TODO SSL

