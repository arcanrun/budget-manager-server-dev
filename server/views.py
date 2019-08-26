from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User, Group
from .models import Vkuser, History
import datetime
import json

from .helpers import get_updated_data, make_calculations, make_calculations_full,  costsPattern, history_saver, next_pay_day

from .calculations.plus_or_minus_budget import plus_or_minus_budget
from .calculations.first_add_or_change_budget import first_add_or_change_budget
from .calculations.set_new_pay_date import set_new_pay_date
from .calculations.plus_minus_transfer_for_50_30_20 import plus_minus_transfer_for_50_30_20

from .auth.log_in_by_vk_id import log_in_by_vk_id
from .auth.sign_up_by_vk_id import sign_up_by_vk_id

from .staistics.get_costs_all import get_costs_all
from .staistics.get_history import get_history
from .staistics.get_stat_for_current_month import get_stat_for_current_month

from .profile.profile_settings import profile_settings

from .profile.change_tutorial_state import change_tutorial_state


def log_in(request):
    return log_in_by_vk_id(request)


def sign_up(request):
    return sign_up_by_vk_id(request)


def add_or_change_budget(request):
    return first_add_or_change_budget(request)


def calc_budget(request):
    return plus_or_minus_budget(request)


def add_payday(request):
    return set_new_pay_date(request)


def manager_page(request):
    return get_costs_all(request)


def temp_today_cost(request):
    return plus_minus_transfer_for_50_30_20(request)


def history_page(request):
    return get_history(request)


def profile_manage(request):
    return profile_settings(request)


def profile_page(request):
    return get_stat_for_current_month(request)


def tutorial_state(request):
    return change_tutorial_state(request)
