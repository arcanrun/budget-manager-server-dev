from django.shortcuts import render
from .models import Vkuser
from django.http import JsonResponse
from django.contrib.auth.models import User, Group
from .models import Vkuser, History
import datetime

from .helpers import get_updated_data, make_calculations, costsPattern, history_saver, next_pay_day

import json


def add_budget(request):
    req = json.loads(str(request.body, encoding='utf-8'))

    vk_id = str(req['vk_id'])
    budget = round(float(req['budget']), 2)
    operation = str(req['operation'])

    all_users = Vkuser.objects.all()

    if operation == 'add':
        print('[add_budget:RECIVED]-->', req)
        for field in all_users:
            if (vk_id == field.id_vk):
                Vkuser.objects.filter(id_vk=vk_id).update(
                    budget=budget)
                break
        response = get_updated_data(vk_id)
        print('[add_budget:RESPONSE]-->', response)
        return JsonResponse(response)

    if operation == 'change':
        print('[change_budget:RECIVED]-->', req)
        daysToPayday = req['daysToPayday']
        for field in all_users:
            if (vk_id == field.id_vk):

                resArr = make_calculations(
                    field.common, field.fun, field.invest, field.days_to_payday, budget)
                Vkuser.objects.filter(id_vk=vk_id).update(
                    budget=budget, common=resArr[0], fun=resArr[1], invest=resArr[2])
                break
        response = get_updated_data(vk_id)
        response['TEST'] = resArr
        print('[change_budget:RESPONSE]-->', response)

        return JsonResponse(response)


def add_payday(request):
    req = json.loads(str(request.body, encoding='utf-8'))
    print('[add_payday:RECIVED]-->', req)
    response = {'RESPONSE': 'ERROR', 'PAYLOAD': {}}

    vk_id = str(req['vk_id'])
    pay_day = str(req['payday'])
    days_to_payday = int(req['days_to_payday'])

    all_users = Vkuser.objects.all()

    for field in all_users:
        if (vk_id == field.id_vk):

            resArr = make_calculations(
                field.common, field.fun, field.invest, days_to_payday,  field.budget)

            Vkuser.objects.filter(id_vk=vk_id).update(
                pay_day=pay_day, days_to_payday=days_to_payday, common=resArr[0], fun=resArr[1], invest=resArr[2])
            break

    response = get_updated_data(vk_id)
    response['TEST'] = resArr
    print('[add_payday:RESPONSE]-->', response)

    return JsonResponse(response)


def get_costs_all(request):
    req = json.loads(str(request.body, encoding='utf-8'))
    print('[get_costs_all:RECIVED]-->', req)
    response = {'RESPONSE': 'ERROR', 'PAYLOAD': {
    }}
    vk_id = str(req['vk_id'])
    toDay = datetime.datetime.strptime(req['toDay'][:10], '%Y-%m-%d')
    daysToPayday_check = 0

    all_users = Vkuser.objects.all()
    for field in all_users:
        if (vk_id == field.id_vk):
            pay_day_formated = field.pay_day[:10]
            if pay_day_formated != "":  # checker for first time user has been logged in
                daysToPayday_check = (datetime.datetime.strptime(
                    pay_day_formated, '%Y-%m-%d') - toDay)
                daysToPayday_check = daysToPayday_check.days

                if daysToPayday_check != int(field.days_to_payday):
                    if daysToPayday_check <= 0:
                        next_payday = next_pay_day(field.pay_day)
                        next_daysToPay = next_payday - toDay
                        next_daysToPay = next_daysToPay.days
                        print('-------------------', next_daysToPay)
                        Vkuser.objects.filter(id_vk=vk_id).update(
                            days_to_payday=next_daysToPay, pay_day=next_payday)
                        daysToPayday_check = next_daysToPay
                    else:
                        Vkuser.objects.filter(id_vk=vk_id).update(
                            days_to_payday=daysToPayday_check)

                    resArr = make_calculations(
                        field.common, field.fun, field.invest, daysToPayday_check,  field.budget)

                    Vkuser.objects.filter(id_vk=vk_id).update(
                        common=resArr[0], fun=resArr[1], invest=resArr[2])
                    break

    response = get_updated_data(vk_id)
    print('[get_costs_all:RESPONSE]-->', response)
    return JsonResponse(response)


def log_in(request):
    req = json.loads(str(request.body, encoding='utf-8'))
    print('[log_in:RECIVED]-->', req)

    vk_id = str(req['vk_id'])
    name = str(req['name'])
    sure_name = str(req['sure_name'])
    avatar = str(req['avatar'])

    response = {'RESPONSE': 'LOGIN_ERROR', 'PAYLOAD': {}
                }

    all_users = Vkuser.objects.all()
    for field in all_users:
        if (vk_id == field.id_vk):
            response['RESPONSE'] = 'ALREADY_HERE'
            response['PAYLOAD']['vk_id'] = field.id_vk
            response['PAYLOAD']['name'] = name
            response['PAYLOAD']['sure_name'] = sure_name
            response['PAYLOAD']['avatar'] = avatar

            print('[log_in:RESPONSE]-->', response)
            return JsonResponse(response)

    # user = Vkuser(id_vk=vk_id, common=costsPattern,
    #               fun=costsPattern, invest=costsPattern)
    # user.save()

    print('[log_in:RESPONSE]-->', response)

    return JsonResponse(response)


def sign_up(request):
    req = json.loads(str(request.body, encoding='utf-8'))
    response = {'RESPONSE': 'SIGN_UP_ERROR', 'PAYLOAD': False
                }

    vk_id = str(req['vk_id'])
    name = str(req['name'])
    sure_name = str(req['sure_name'])
    avatar = str(req['avatar'])
    register_date = req['toDay']

    print('[sign_up:RECIVED]-->', req)
    user = Vkuser(id_vk=vk_id, common=costsPattern,
                  fun=costsPattern, invest=costsPattern, register_date=register_date)
    user.save()

    response['RESPONSE'] = 'SIGN_UP_SUCCESS'
    response['PAYLOAD'] = {}
    response['PAYLOAD']['vk_id'] = vk_id
    response['PAYLOAD']['name'] = name
    response['PAYLOAD']['sure_name'] = sure_name
    response['PAYLOAD']['avatar'] = avatar

    print('[sign_up:RESPONSE]-->', response)
    return JsonResponse(response)


def temp_today_cost(request):
    req = json.loads(str(request.body, encoding='utf-8'))
    print('[temp_today_cost:RECIVED]-->', req)

    vk_id = str(req['vk_id'])
    typeCost = req['type']
    value = round(float(req['value']), 2)
    operation = req['operation']
    date_now = req['date_now']
    newBudget = ''
    costsObject = {}
    all_users = Vkuser.objects.all()
    for field in all_users:
        if (vk_id == field.id_vk):

            costsObject["common"] = json.loads(field.common)
            costsObject["fun"] = json.loads(field.fun)
            costsObject["invest"] = json.loads(field.invest)

            if operation == 'plus':
                newBudget = float(field.budget) + value
                costsObject[typeCost]['temp'] = round(
                    costsObject[typeCost]['temp'] + value, 2)
            if operation == 'minus':
                newBudget = float(field.budget) - value
                costsObject[typeCost]['temp'] = round(
                    costsObject[typeCost]['temp'] - value, 2)
            history_saver(field.id_vk, date_now, operation, value, typeCost)

            Vkuser.objects.filter(id_vk=vk_id).update(
                budget=round(newBudget, 2), common=json.dumps(costsObject["common"]), fun=json.dumps(costsObject["fun"]), invest=json.dumps(costsObject["invest"]))
            break

    response = get_updated_data(vk_id)
    print('[temp_today_cost:RESPONSE]-->', response)

    return JsonResponse(response)


def get_history(request):
    response = {'RESPONSE': 'ERROR', 'PAYLOAD': []}
    req = json.loads(str(request.body, encoding='utf-8'))
    print('[get_history:RECIVED]-->', req)
    vk_id = str(req['vk_id'])

    history = History.objects.all()
    history_object = {}
    tempArr = []
    cost_object = {'type_cost': '', 'operation': '', 'value': ''}

    for field in history:
        if (vk_id == field.id_vk):
            if field.date in history_object:
                cost_object['type_cost'] = field.type_costs
                cost_object['value'] = field.value
                cost_object['operation'] = field.operation

            else:
                history_object[field.date] = []

                cost_object['type_cost'] = field.type_costs
                cost_object['value'] = field.value
                cost_object['operation'] = field.operation

            history_object[field.date].append(cost_object)

            cost_object = {'type_cost': '', 'operation': '', 'value': ''}

    for k, v in history_object.items():
        v.reverse()
        response['PAYLOAD'].append({k: v})

    response['RESPONSE'] = 'SUCCESS'

    print('[get_history:RESPONSE]-->', response)

    return JsonResponse(response)


def profile_manage(request):
    response = {'RESPONSE': 'ERROR', 'PAYLOAD': 'ERROR'}
    req = json.loads(str(request.body, encoding='utf-8'))
    print('[profile_manage:RECIVED]-->', req)

    vk_id = str(req['vk_id'])
    operation = req['operationType']

    all_users = Vkuser.objects.all()
    history = History.objects.all()

    if operation == 'delete':
        for field in all_users:
            if (vk_id == field.id_vk):
                Vkuser.objects.filter(id_vk=vk_id).delete()
        for field in history:
            if (vk_id == field.id_vk):
                History.objects.filter(id_vk=vk_id).delete()
        response = {'RESPONSE': 'DELETE_USER_SUCCESS',
                    'PAYLOAD': 'DELETE_USER_SUCCESS'}
    print('[profile_manage:RESPONSE]-->', response)
    return JsonResponse(response)


def get_statistics(request):
    response = {'RESPONSE': 'ERROR', 'PAYLOAD': {}}
    req = json.loads(str(request.body, encoding='utf-8'))
    print('[get_statistics:RECIVED]-->', req)

    vk_id = str(req['vk_id'])

    toDayMonth = req['toDayFormated'][3:]
    costs = {
        'total': 0,
        'common': 0,
        'fun': 0,
        'invest': 0,
    }
    income = {
        'total': 0,
        'common': 0,
        'fun': 0,
        'invest': 0,
    }

    history = History.objects.all()
    for field in history:
        if (vk_id == field.id_vk and field.date[3:] == toDayMonth):
            if field.operation == 'minus':
                costs['total'] += float(field.value)
                if field.type_costs == 'common':
                    costs['common'] += float(field.value)
                if field.type_costs == 'fun':
                    costs['fun'] += float(field.value)
                if field.type_costs == 'invest':
                    costs['invest'] += float(field.value)
            if field.operation == 'plus':
                income['total'] += float(field.value)
                if field.type_costs == 'common':
                    income['common'] += float(field.value)
                if field.type_costs == 'fun':
                    income['fun'] += float(field.value)
                if field.type_costs == 'invest':
                    income['invest'] += float(field.value)
    response['RESPONSE'] = 'FETCHED_STATISTICS_SUCCESS'
    response['PAYLOAD']['costs'] = costs
    response['PAYLOAD']['income'] = income

    print('[get_statistics:RESPONSE]-->', response)
    return JsonResponse(response)
