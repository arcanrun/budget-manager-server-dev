from django.contrib.auth.models import User, Group
from .models import Vkuser, History
import datetime
import calendar

import json

costsPattern = json.dumps({
    "value": "",
    "maxToday": "",
    "temp": ""
})


def is_user_registered(user_id: str)->bool:
    all_users = Vkuser.objects.all()
    for field in all_users:
        if (user_id == field.id_vk):
            return True
    return False


def get_id_from_vk_params(params: str)->str:
    pos_0 = params.find('vk_user_id=') + len('vk_user_id=')
    cut_params = params[pos_0:]
    pos_1 = cut_params.find('&')
    vk_id = cut_params[:pos_1]
    return vk_id


def get_updated_data(vk_id):
    response = {'RESPONSE': 'ERROR', 'PAYLOAD': {}}
    updated_all_users = Vkuser.objects.all()
    for field in updated_all_users:
        if (vk_id == field.id_vk):
            response['PAYLOAD']['common'] = json.loads(field.common)
            response['PAYLOAD']['fun'] = json.loads(field.fun)
            response['PAYLOAD']['invest'] = json.loads(field.invest)
            response['PAYLOAD']['budget'] = field.budget
            response['PAYLOAD']['pay_day'] = field.pay_day
            response['PAYLOAD']['days_to_payday'] = field.days_to_payday
            response['PAYLOAD']['register_date'] = field.register_date
            response['PAYLOAD']['is_tutorial_done'] = field.is_tutorial_done
            response['RESPONSE'] = 'SUCCES_FETCHED'

    return response


def next_pay_day(current_pay_day):
    currentFormated = datetime.datetime.strptime(
        current_pay_day[:10], '%Y-%m-%d')

    month = currentFormated.month
    year = currentFormated.year + month // 12
    month = month % 12 + 1
    day = min(currentFormated.day, calendar.monthrange(year, month)[1])

    return datetime.datetime(year, month, day)


def make_calculations(field_common, filed_fun, filed_invest, daysToPayday, budget):
    """difference between make_calcualtions and make_caculations_full 
    IS that make_calculations is for temp costs only and FULL is for relodaing all"""
    daysToPayday = int(daysToPayday)

    commonObject = json.loads(field_common)
    funObject = json.loads(filed_fun)
    investObject = json.loads(filed_invest)

    common = commonObject['value']
    fun = funObject['value']
    invest = investObject['value']

    if daysToPayday == 0:
        commonObject["maxToday"] = commonObject['value']
        funObject["maxToday"] = funObject['value']
        investObject["maxToday"] = investObject['value']
    else:
        commonObject["maxToday"] = round((
            float(common)) / daysToPayday, 2)
        funObject["maxToday"] = round((
            float(fun)) / daysToPayday, 2)
        investObject["maxToday"] = round((
            float(invest) * 0.2) / daysToPayday, 2)

    commonObject["temp"] = commonObject["maxToday"]
    funObject["temp"] = funObject["maxToday"]
    investObject["temp"] = investObject["maxToday"]

    commonObjectJSON = json.dumps(commonObject)
    funObjectJSON = json.dumps(funObject)
    investObjectJSON = json.dumps(investObject)
    return [commonObjectJSON, funObjectJSON, investObjectJSON]


def make_calculations_full(field_common, filed_fun, file_invest, daysToPayday, budget):

    daysToPayday = int(daysToPayday)

    commonObject = json.loads(field_common)
    funObject = json.loads(filed_fun)
    investObject = json.loads(file_invest)

    commonObject['value'] = round((float(budget) * 0.5), 2)
    funObject['value'] = round((float(budget) * 0.3), 2)
    investObject['value'] = round((float(budget) * 0.2), 2)
    if daysToPayday == 0:
        commonObject["maxToday"] = commonObject['value']
        funObject["maxToday"] = funObject['value']
        investObject["maxToday"] = investObject['value']
    else:
        commonObject["maxToday"] = round((
            float(budget) * 0.5) / daysToPayday, 2)
        funObject["maxToday"] = round((
            float(budget) * 0.3) / daysToPayday, 2)
        investObject["maxToday"] = round((
            float(budget) * 0.2) / daysToPayday, 2)

    commonObject["temp"] = commonObject["maxToday"]
    funObject["temp"] = funObject["maxToday"]
    investObject["temp"] = investObject["maxToday"]

    commonObjectJSON = json.dumps(commonObject)
    funObjectJSON = json.dumps(funObject)
    investObjectJSON = json.dumps(investObject)
    return [commonObjectJSON, funObjectJSON, investObjectJSON]


def history_saver(id_vk, date, operation, value, type_costs):
    history = History(id_vk=id_vk, date=date,
                      operation=operation, value=value, type_costs=type_costs)
    history.save()
    print('[history]:SUCCESS')
