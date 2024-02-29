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
    sub_cat = models.ForeignKey(Categories, on_delete=models.CASCADE)
    sub_name = models.CharField(max_length=200, help_text='Добавь новую подкатегорию')

    def __str__(self):
        return f'{self.sub_cat} {self.sub_name}'


class Masters(models.Model):
    master_id = models.AutoField(primary_key=True)
    sub_master = models.ForeignKey(Subcategories, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, help_text='Имя')
    specialization = models.CharField(max_length=500, help_text='Имя', default=None, null=True, blank=True)
    phone = models.CharField(max_length=10, help_text='Контактный номер телефона', default=None, null=True, blank=True)
    address = models.CharField(max_length=500, help_text='Адрес, при наличии', default=None, null=True, blank=True)
    tg = models.CharField(max_length=20, help_text='Ник или ссылка на telegram', default=None, null=True, blank=True)
    wa = models.CharField(max_length=20, help_text='Ник или ссылка на whatsapp', default=None, null=True, blank=True)
    ig = models.CharField(max_length=20, help_text='Ник или ссылка на instagram', default=None, null=True, blank=True)
    vk = models.CharField(max_length=20, help_text='Ник или ссылка на vk', default=None, null=True, blank=True)
    password = models.CharField(max_length=20, editable=False, unique=True)
    visability = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.master_id}, {self.sub_master}, {self.name}, {self.specialization}, {self.phone}, {self.address}, {self.tg}, \
               {self.wa}, {self.ig}, {self.visability}, {self.password}'


class Images(models.Model):
    img_id = models.AutoField(primary_key=True)
    master_img = models.ForeignKey(Masters, on_delete=models.CASCADE)
    img_path = models.ImageField()

    def __str__(self):
        return f'{self.img_id}, {self.master_img}, {self.img_path}'


class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    admin_name = models.CharField(max_length=200, help_text='Имя')
    admin_password = models.CharField(max_length=20, help_text='Пароль')

    def __str__(self):
        return f'{self.admin_id}, {self.admin_name}, {self.admin_password}'