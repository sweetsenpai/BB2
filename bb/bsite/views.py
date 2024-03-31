import django.utils.datastructures
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Categories, Subcategories, Masters, Admin, Images
from django.core.exceptions import ObjectDoesNotExist
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
import codecs
from .image_upload import upload_image, storage
import secrets
import string


def create_password():
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(19))
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
            subcat_update.save()
        elif request.POST.get('add_button') is not None:
            if request.POST.get('newdata') != '':
                new_subcat = Subcategories(sub_cat=Categories.objects.get(cat_id=pk), sub_name=request.POST.get('newdata'))
                new_subcat.save()
    return HttpResponse(template.render(records, request))


def masters(request):
    records = {'masters': Masters.objects.all().order_by('-master_id')}
    template = loader.get_template('masters.html')
    if request.method == 'POST':
        if request.POST.get('add_button') is not None:
            if request.POST.get('newdata') != '':
                new_master = Masters(name=request.POST.get('newdata'), username=create_password(), password=create_password())
                new_master.save()
        elif request.POST.get('delete_button') is not None:
            Masters.objects.get(master_id=request.POST.get('delete_button')).delete()
        elif request.POST.get('change_button') is not None:

            if not request.POST.getlist('visability'):
                visability = False
            else:
                visability = True
            master = Masters.objects.get(master_id=request.POST.get('change_button'))
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
                new_master = Masters(name=request.POST.get('newdata'), username=create_password(), password=create_password())
                sub = Subcategories.objects.get(sub_id=pk)
                new_mastert.save()
                new_master.sub_master.add(sub)
                new_master.save()
        if request.POST.get('change_button') is not None:
            if not request.POST.getlist('visability'):
                visability = False
            else:
                visability = True
            master = Masters.objects.get(master_id=request.POST.get('change_button'))
            master.visability = visability
            master.save()
    return HttpResponse(template.render(records, request))


def master_page(request, pk):
    if request.user.is_authenticated:
        master = Masters.objects.get(master_id=pk)
        records = {'masters': [master]}
        if request.user.is_superuser:
            s_m = master.sub_master.all()
            connected_subs = []
            for sub in s_m:
                connected_subs.append(sub.sub_name)
            records['connected'] = connected_subs
            template = loader.get_template('master_page_admin.html')
        else:
            template = loader.get_template('master_page.html')
        return HttpResponse(template.render(records, request))
    else:
        return redirect('not_authorized')


def settings(request, pk):
    if request.user.is_superuser:
        template = loader.get_template('admin_settings.html')
    elif request.user.is_authenticated:
        template = loader.get_template('settings.html')
    else:
        return redirect('not_authorized')

    master = Masters.objects.get(master_id=pk)
    s_m = master.sub_master.all()
    connected_subs = []
    for sub in s_m:
        connected_subs.append(sub.sub_name)

    records = {'masters': [master], 'subcategories': Subcategories.objects.all().order_by('sub_id').values(), 'connected': connected_subs}
    if request.method == 'POST':
        checked_subs = request.POST.getlist('sub')

        for sub_id in checked_subs:
            sub = Subcategories.objects.get(sub_id=sub_id)
            master.sub_master.add(sub)
            master.save()

        for sub_name in connected_subs:
            sub = Subcategories.objects.get(sub_name=sub_name)
            if str(sub.sub_id) not in checked_subs:
                master.sub_master.remove(sub)

        if request.POST.get('name') is not None or str(request.POST.get('name')).replace(' ', '') != '' or master.name != request.POST.get('name'):
            master.name = request.POST.get('name')
        if request.POST.get('phone') is not None or str(request.POST.get('phone')).replace(' ', '') != '' or master.phone != request.POST.get('phone'):
            master.phone = request.POST.get('phone')
        if request.POST.get('address') is not None or str(request.POST.get('address')).replace(' ', '') != '' or master.address != request.POST.get('address'):
            master.address = request.POST.get('address')
        if request.POST.get('info') is not None or str(request.POST.get('info')).replace(' ', '') != '' or master.info != request.POST.get('info'):
            master.info = request.POST.get('info')
        if request.POST.get('tg') is not None or str(request.POST.get('tg')).replace(' ', '') != '' or master.tg != request.POST.get('tg'):
            master.tg = request.POST.get('tg')
        if request.POST.get('vk') is not None or str(request.POST.get('vk')).replace(' ', '') != '' or master.vk != request.POST.get('vk'):
            master.vk = request.POST.get('vk')
        if request.POST.get('wa') is not None or str(request.POST.get('wa')).replace(' ', '') != '' or master.wa != request.POST.get('wa'):
            master.wa = request.POST.get('wa')
        if request.POST.get('ig') is not None or str(request.POST.get('ig')).replace(' ', '') != '' or master.ig != request.POST.get('ig'):
            master.ig = request.POST.get('ig')
        master.need_moderation = True
        master.need_moderation = False
        master.save()
        return redirect(f'/bsite/master_page/{pk}')
    return HttpResponse(template.render(records, request))


def gallery(request, pk):

    master_images = Images.objects.filter(master_img=pk).all().values()
    context = {'images': master_images}
    if request.method == 'POST':
        if request.POST.get('back') is not None:
            return redirect(f'/bsite/master_page/{pk}')
        if request.POST.get('delete_button') is not None:
            image_delet = Images.objects.get(img_id=request.POST.get('delete_button'))
            storage.delete_file(file_id=image_delet.file_id)
            Images.objects.get(img_id=request.POST.get('delete_button')).delete()
        else:
            try:
                file_data = request.FILES['file'].file.read()

                encoded_data = codecs.encode(file_data, 'base64')
                upload_img_data = upload_image(image_data=encoded_data, file_name=f'{pk}_{len(master_images) + 1}.jpg')
                description = request.POST.get('description')
                new_image = Images(master_img=Masters.objects.get(master_id=pk), img_url=upload_img_data[0], file_id=upload_img_data[1], description=description)
                new_image.save()
            except django.utils.datastructures.MultiValueDictKeyError:
                pass

        return redirect(f'/bsite/master_page/gallery/{pk}')
    return render(request, 'gallery.html', context)


def logginpage(request):
    context = {}
    if request.method == 'POST':
        if request.POST.get('username') is not None and request.POST.get('password') is not None:
            name = request.POST.get('username')
            password = request.POST.get('password')
            try:
                admin = Admin.objects.get(admin_name=name, admin_password=password)
                user = authenticate(username=admin.admin_name, password=admin.admin_password)
                if user is None:
                    User.objects.create_superuser(username=admin.admin_name, password=admin.admin_password)
                    user = authenticate(username=admin.admin_name, password=admin.admin_password)
                login(request, user)
                return redirect('index_page')
            except ObjectDoesNotExist:
                try:
                    master = Masters.objects.get(name=name, password=password)
                    user = authenticate(username=master.username, password=master.password)
                    if user is None:
                        User.objects.create_user(username=master.username, password=master.password)
                        user = authenticate(username=master.username, password=master.password)
                    login(request, user)
                    return redirect(f'/bsite/master_page/{master.master_id}')
                except ObjectDoesNotExist:
                    messages.success(request, 'Имя пользователя или пароль не найдены!')
    return render(request, 'loggin.html', context)


def logoutpage(request):
    logout(request)
    return redirect('logginpage')


def not_authorized(request):
    return redirect('logginpage')


# TODO дебаг страницы настроек для мастера и админа
# TODO тест всего приложения
# TODO БОТ
# TODO ХОСТИНГ
# TODO SSL

