from django.urls import path
from . import views

urlpatterns = [
    path('loggin', views.logginpage, name='logginpage'),
    path('', views.index_page, name='index_page'),
    path('master', views.master_page, name='master_page'),
    path('error', views.not_authorized, name='not_authorized'),
    path('subcat', views.subcat_all, name='subcat_all'),
    path('subcategories/<int:pk>', views.subcat_dv, name='subcats'),
    path('masters', views.masters, name='masters'),
    path('masters/<int:pk>', views.masters_dv, name='masters_dv'),
    path('images', views.images, name='images'),
    path('master_page/<int:pk>', views.master_page)
]
