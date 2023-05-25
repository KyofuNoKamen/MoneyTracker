from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import routers

from . import views

urlpatterns = [
    path('', views.home, name=''),
    path('home', views.home, name='home'),
    path('profile', views.profile, name='profile'),
    path('adding/', views.adding, name='adding'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('export/', views.export, name='export'),
    path('style.css', TemplateView.as_view(
        template_name='style.css',
        content_type='text/css')
        ),
    path('main.css', TemplateView.as_view(
        template_name='style.css',
        content_type='text/css')
         ),

    path('export/excel', views.export_income_xls, name='export_excel'),
]