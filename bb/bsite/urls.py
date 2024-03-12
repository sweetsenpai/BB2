from django.urls import path
from . import views

urlpatterns = [
    path('loggin', views.logginpage, name='logginpage'),
    path('logout', views.logoutpage, name='logoutpage'),
    path('', views.index_page, name='index_page'),
    path('error', views.not_authorized, name='not_authorized'),
    path('subcat', views.subcat_all, name='subcat_all'),
    path('subcategories/<int:pk>', views.subcat_dv, name='subcats'),
    path('masters', views.masters, name='masters'),
    path('masters/<int:pk>', views.masters_dv, name='masters_dv'),
    path('master_page/<int:pk>', views.master_page),
    path('master_page/gallery/<int:pk>/', views.gallery, name='images'),
    path('master_page/settings/<int:pk>', views.settings)
]
