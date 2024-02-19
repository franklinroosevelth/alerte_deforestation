"""
URL configuration for alerte_foret project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import *
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='authentication-login.html'), name="login_page"),
    path('confirmer_action', TemplateView.as_view(template_name='authentication-login.html'), name="confirmer_action"),
    path('accueil', home_page, name="accueil"),
    path('detail_alerte', detail_alerte, name="detail_alerte"),
    path('signaler_alerte', signaler_alerte, name="signaler_alerte"),
    path('capture', capture_page, name="capture"),
    path('login', se_connecter, name="login"),
    path('logout', se_deconnecter, name="logout"),
    path('list_users', users_page, name="list_users"),
    path('detail_user', detail_user, name="detail_user"),
    path('save_user', save_user, name="save_user"),
    path('save_capture', save_capture, name="save_capture"),
    path('save_capture', save_capture, name="save_capture"),
    path('creer_user', TemplateView.as_view(template_name='creer_user.html'), name="creer_user"),
]