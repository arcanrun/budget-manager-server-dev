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
from django.conf.urls import url, include
from server import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('add-or-change-budget/', views.add_or_change_budget),  # done
    path('add-payday/', views.add_payday),  # done
    path('manager-page/', views.manager_page),  # done
    path('temp-today-cost/', views.temp_today_cost),  # done
    path('log-in/', views.log_in),  # done
    path('sign-up/', views.sign_up),  # done
    path('history-page/', views.history_page),  # done
    path('history-short/', views.history_short_info),
    path('profile-manage/', views.profile_manage),  # done
    path('profile_page/', views.profile_page),  # done
    path('calc-budget/', views.calc_budget),  # done
    path('tutorial-state/', views.tutorial_state),  # done
    path('vk_client_theme/', views.toggle_vk_theme),  # done
    path('custom_dark_theme/', views.toggle_custom_dark_theme),  # done
    path('enter-data/', views.enter_data),  # done
    path('/', include('rest_framework.urls'))

]
