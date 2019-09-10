"""
All statics for main page 'Manager'
"""

import json
from django.http import JsonResponse
import datetime
from ..models import Vkuser, History

from ..helpers import get_updated_data, make_calculations, make_calculations_full,  costsPattern, history_saver, next_pay_day, get_id_from_vk_params, is_user_registered, set_days_to_payday

from ..auth.chcek_sign import is_valid, insert_client_sign, make_dict_from_query


def get_costs_all(request):
    req = json.loads(str(request.body, encoding='utf-8'))
    print('[get_costs_all:RECIVED]-->', req)
    response = {'RESPONSE': 'AUTH_ERROR', 'PAYLOAD': {
    }}
    vk_id = get_id_from_vk_params(str(req['params']))
    query_params = make_dict_from_query(str(req['params']))
    client_secret = insert_client_sign()

    if is_valid(query=query_params, secret=client_secret):
        payday_and_values = set_days_to_payday(vk_id, str(req['toDay']))
        resArr = make_calculations_full(
            payday_and_values['common'], payday_and_values['fun'], payday_and_values['invest'], payday_and_values['days_to_payday'],  payday_and_values['budget'])

        Vkuser.objects.filter(id_vk=vk_id).update(
            common=resArr[0], fun=resArr[1], invest=resArr[2])
        response = get_updated_data(vk_id)

        print('[get_costs_all:RESPONSE]-->', response)
        return JsonResponse(response)
    else:
        print('[get_costs_all:RESPONSE]-->', response)
        return JsonResponse(response)
