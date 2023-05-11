from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('style.css', TemplateView.as_view(
        template_name='style.css',
        content_type='text/css')
        ),
    path('main.css', TemplateView.as_view(
        template_name='style.css',
        content_type='text/css')
         ),
]