"""
Plus and Minus buttons for budget card
"""
import json
from django.http import JsonResponse
from ..models import Vkuser, History

from ..helpers import get_updated_data, make_calculations, make_calculations_full,  costsPattern, history_saver, next_pay_day, get_id_from_vk_params, is_user_registered

from ..auth.chcek_sign import is_valid, insert_client_sign, make_dict_from_query


def plus_or_minus_budget(request):

    response = {'RESPONSE': 'AUTH_ERROR', 'PAYLOAD': {}}
    req = json.loads(str(request.body, encoding='utf-8'))
    print('[calc_budget:RECIVED]-->', req)

    vk_id = get_id_from_vk_params(str(req['params']))
    query_params = make_dict_from_query(str(req['params']))
    client_secret = insert_client_sign()
    if is_valid(query=query_params, secret=client_secret):
        value = round(float(req['value']), 2)
        operation = req['operation']
        date_now = req['date_now']
        type = req['type']

        all_users = Vkuser.objects.all()
        for field in all_users:
            if (vk_id == field.id_vk):
                budget = float(field.budget)
                if (operation == 'minus'):
                    budget -= value

                if (operation == 'plus'):
                    budget += value

                resArr = make_calculations_full(
                    field.common, field.fun, field.invest, field.days_to_payday, budget)
                Vkuser.objects.filter(id_vk=vk_id).update(
                    budget=budget, common=resArr[0], fun=resArr[1], invest=resArr[2])

                history_saver(field.id_vk, date_now, operation, value, type)
                break

        response = get_updated_data(vk_id)
        print('[calc_budget:RESPONSE]-->', response)

        return JsonResponse(response)
    else:
        print('[calc_budget:RESPONSE]-->', response)

        return JsonResponse(response)
