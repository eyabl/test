"""djangoProject2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include

from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.red, name='index'),
    path('dashboard', views.index, name='dashboard'),
    path('load', views.load, name='load'),
    path('load2', views.load2, name='load2'),
    path('open', views.open, name='open'),
    path('lovgest', views.lovgest, name='lovgest'),
    path('lovgest/modifier/<int:id>', views.update, name='modifier'),
    path('lovgest/supprimer/<int:id>', views.delete, name='supprimer'),
    path('lovgest/ajouter', views.add, name='ajouter'),
    path('user/', include('django.contrib.auth.urls')),
    path('user/register', views.register, name='register'),
    path('iexp/<int:id>', views.iexp, name='iexp'),
    path('iexp/load', views.loadiexp, name='loadiexp'),
]
