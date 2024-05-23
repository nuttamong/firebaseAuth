"""
URL configuration for auth_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
# from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from page import views

urlpatterns = [
    path('', views.LoginPage),
    path('home/', views.HomePage, name="home"),
    path('login/', views.PostLogin, name="login"),
    path('signUp/', views.PostRegister, name="signUp"),
    path('logout/', views.Logout, name="logout"),
    path('repwd/', views.RePWDPage, name="repwd"),
    path('postReset/', views.postReset, name="postReset"),
    path('delete/', views.Delete, name="delete"),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
