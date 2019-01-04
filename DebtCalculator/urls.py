"""DebtCalculator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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

from debtcalculatorapp.views import *

urlpatterns = [
    path('', index, name='index'),
    path('add/', add, name='add'),
    path('edit_exchange_fees/', edit_exchange_fees, name='edit_exchange_fees'),

    path('summarize/', summarize, name='summarize'),
    path('edit_exchange_rate/', edit_exchange_rate, name='edit_exchange_rate'),

    path('login/', login_form, name='login_form'),
    path('register/', register, name='register'),

    path('admin/', admin.site.urls, name='admin'),
    path('auth/', include('django.contrib.auth.urls')),
]
