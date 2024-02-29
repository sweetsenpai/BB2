from django.contrib import admin
from .models import Categories, Subcategories, Masters, Images, Admin

admin.site.register(Categories)
admin.site.register(Subcategories)
admin.site.register(Masters)
admin.site.register(Images)
admin.site.register(Admin)