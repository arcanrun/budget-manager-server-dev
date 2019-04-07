"""backend URL Configuration

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
from django.urls import path
from server import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('add-budget/', views.add_budget),
    path('add-payday/', views.add_payday),
    path('get-costs-all/', views.get_costs_all),
    path('temp-today-cost/', views.temp_today_cost),
    path('log-in/', views.log_in),
    path('sign-up/', views.sign_up),
    path('get-history/', views.get_history),
    path('profile-manage/', views.profile_manage),
    path('get-statistics/', views.get_statistics),
]
