from django.db import models
from django.conf import settings
import secrets
import string


class Categories(models.Model):
    cat_id = models.AutoField(primary_key=True)
    cat_name = models.CharField(max_length=200, help_text='Добавь новую категорию')

    def __str__(self):
        return f'{self.cat_name}'


class Subcategories(models.Model):
    sub_id = models.AutoField(primary_key=True)
    sub_cat = models.ForeignKey(Categories, on_delete=models.CASCADE,)
    sub_name = models.CharField(max_length=200, help_text='Добавь новую подкатегорию')

    def __str__(self):
        return f'{self.sub_cat} {self.sub_name}'


class Masters(models.Model):
    master_id = models.AutoField(primary_key=True)
    sub_master = models.ManyToManyField(Subcategories)
    name = models.CharField(max_length=200, help_text='Имя')
    info = models.TextField(help_text='Дополнительная информация', default=None, null=True, blank=True)
    phone = models.CharField(max_length=20, help_text='Контактный номер телефона', default=None, null=True, blank=True)
    address = models.CharField(max_length=500, help_text='Адрес, при наличии', default=None, null=True, blank=True)
    tg = models.CharField(max_length=50, help_text='Ник или ссылка на telegram', default=None, null=True, blank=True)
    wa = models.CharField(max_length=50, help_text='Ник или ссылка на whatsapp', default=None, null=True, blank=True)
    ig = models.CharField(max_length=50, help_text='Ник или ссылка на instagram', default=None, null=True, blank=True)
    vk = models.CharField(max_length=50, help_text='Ник или ссылка на vk', default=None, null=True, blank=True)
    password = models.CharField(max_length=20, editable=False)
    username = models.CharField(max_length=20, editable=False, default=None, null=True)
    visability = models.BooleanField(default=False)
    need_moderation = models.BooleanField(default=False, null=True, blank=True)
    msg_sended = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return f'{self.master_id}, {self.sub_master}, {self.name}, {self.phone}, {self.address}, {self.tg}, ' \
               f'{self.wa}, {self.ig}, {self.visability},{self.username},{self.password},({", ".join(subcategories.sub_name for subcategories in self.sub_master.all())})'


class Images(models.Model):
    img_id = models.AutoField(primary_key=True)
    master_img = models.ForeignKey(Masters, on_delete=models.CASCADE)
    img_url = models.CharField(max_length=100, default=None)
    file_id = models.CharField(max_length=100, default=None)
    telegram_file_id = models.CharField(max_length=100, default=None, null=True, blank=True)
    description = models.TextField(default=None)

    def __str__(self):
        return f'{self.img_id}, {self.master_img}, {self.img_url}, {self.description}'


class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    admin_name = models.CharField(max_length=200, help_text='Имя')
    admin_password = models.CharField(max_length=20, help_text='Пароль')

    def __str__(self):
        return f'{self.admin_id}, {self.admin_name}, {self.admin_password}'