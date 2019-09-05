import json
from django.http import JsonResponse
from ..models import Vkuser, History
from ..helpers import get_updated_data, make_calculations, make_calculations_full,  costsPattern, history_saver, next_pay_day, get_id_from_vk_params, is_user_registered

from ..auth.chcek_sign import is_valid, insert_client_sign, make_dict_from_query


def sign_up_by_vk_id(request):
    req = json.loads(str(request.body, encoding='utf-8'))
    response = {'RESPONSE': 'SIGN_UP_ERROR', 'PAYLOAD': False}

    vk_id = get_id_from_vk_params(str(req['params']))
    query_params = make_dict_from_query(str(req['params']))
    name = str(req['name'])
    sure_name = str(req['sure_name'])
    register_date = req['toDay']
    client_secret = insert_client_sign()

    print('[sign_up_by_vk_id:RECIVED]-->', req)

    if is_valid(query=query_params, secret=client_secret) and not is_user_registered(vk_id):
        user = Vkuser(id_vk=vk_id, name=name, sure_name=sure_name, common=costsPattern,
                      fun=costsPattern, invest=costsPattern, register_date=register_date)
        user.save()

        response['RESPONSE'] = 'SIGN_UP_SUCCESS'
        response['PAYLOAD'] = {}
        response['PAYLOAD']['vk_id'] = vk_id
        response['PAYLOAD']['name'] = name
        response['PAYLOAD']['sure_name'] = sure_name
        response['PAYLOAD']['is_tutorial_done'] = False

        print('[sign_up_by_vk_id:RESPONSE]-->', response)
        return JsonResponse(response)
    else:
        print('[sign_up_by_vk_id:RESPONSE]-->', response)
        return JsonResponse(response)
