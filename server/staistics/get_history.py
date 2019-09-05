"""
Used for history page
"""
import json
from django.http import JsonResponse
import datetime
from ..models import Vkuser, History

from ..helpers import get_updated_data, make_calculations, make_calculations_full,  costsPattern, history_saver, next_pay_day, get_id_from_vk_params, is_user_registered

from ..auth.chcek_sign import is_valid, insert_client_sign, make_dict_from_query


def get_history(request):
    response = {'RESPONSE': 'ERROR_AUTH', 'PAYLOAD': []}
    req = json.loads(str(request.body, encoding='utf-8'))
    print('[get_history:RECIVED]-->', req)
    vk_id = get_id_from_vk_params(str(req['params']))
    query_params = make_dict_from_query(str(req['params']))
    client_secret = insert_client_sign()

    if is_valid(query=query_params, secret=client_secret):
        history = History.objects.all()
        history_object = {}
        tempArr = []
        cost_object = {'type_cost': '', 'operation': '', 'value': '', 'id': ''}

        for field in history:
            if (vk_id == field.id_vk):
                if field.date in history_object:
                    cost_object['type_cost'] = field.type_costs
                    cost_object['value'] = field.value
                    cost_object['operation'] = field.operation
                    cost_object['id'] = field.id
                else:
                    history_object[field.date] = []

                    cost_object['type_cost'] = field.type_costs
                    cost_object['value'] = field.value
                    cost_object['operation'] = field.operation
                    cost_object['id'] = field.id

                history_object[field.date].append(cost_object)

                cost_object = {'type_cost': '',
                               'operation': '', 'value': '', 'id': ''}

        for k, v in history_object.items():
            v.reverse()
            response['PAYLOAD'].append({k: v})
        response['PAYLOAD'].reverse()
        response['RESPONSE'] = 'SUCCESS'

        print('[get_history:RESPONSE]-->', response)

        return JsonResponse(response)

    else:
        print('[get_history:RESPONSE]-->', response)

        return JsonResponse(response)
