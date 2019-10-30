"""
All statics for main page 'Manager'
"""

import json
from django.http import JsonResponse
import datetime
from ..models import Vkuser, History

from ..helpers import logger, get_updated_data, make_calculations, make_calculations_full,  costsPattern, history_saver, next_pay_day, get_id_from_vk_params, is_user_registered, set_days_to_payday

from ..auth.chcek_sign import is_valid, insert_client_sign, make_dict_from_query


def get_costs_all(request):
    req = json.loads(str(request.body, encoding='utf-8'))
    logger('get_costs_all:RECIVED', req)
    response = {'RESPONSE': 'AUTH_ERROR', 'PAYLOAD': {
    }}
    vk_id = get_id_from_vk_params(str(req['params']))
    query_params = make_dict_from_query(str(req['params']))
    client_secret = insert_client_sign()

    if is_valid(query=query_params, secret=client_secret):

        toDay = datetime.datetime.strptime(str(req['toDay'])[:10], '%Y-%m-%d')

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
                            Vkuser.objects.filter(id_vk=vk_id).update(
                                days_to_payday=next_daysToPay, pay_day=next_payday)
                            daysToPayday_check = next_daysToPay
                        else:
                            Vkuser.objects.filter(id_vk=vk_id).update(
                                days_to_payday=daysToPayday_check)

                        resArr = make_calculations_full(
                            field.common, field.fun, field.invest, daysToPayday_check,  field.budget)

                        Vkuser.objects.filter(id_vk=vk_id).update(
                            common=resArr[0], fun=resArr[1], invest=resArr[2])

                        break
        response = get_updated_data(vk_id)
        logger('get_costs_all:RESPONSE', response)
        return JsonResponse(response)
    else:
        logger('get_costs_all:RESPONSE', response)
        return JsonResponse(response)
