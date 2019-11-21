import json
import datetime
from datetime import timedelta
from django.utils import timezone

from django.http import JsonResponse
from ..models import Vkuser, History
from ..helpers import get_updated_data, make_calculations, make_calculations_full,  costsPattern, history_saver, next_pay_day, get_id_from_vk_params, is_user_registered

from ..auth.chcek_sign import is_valid, insert_client_sign, make_dict_from_query


def sign_up_by_vk_id(request):
    req = json.loads(str(request.body, encoding='utf-8'))
    response = {'RESPONSE': 'SIGN_UP_ERROR', 'PAYLOAD': False}

    vk_id = get_id_from_vk_params(str(req['params']))
    query_params = make_dict_from_query(str(req['params']))
    timezone = int(req['timezone'])
    register_date = datetime.datetime.now()
    client_secret = insert_client_sign()

    print('[sign_up_by_vk_id:RECIVED]-->', req)

    if is_valid(query=query_params, secret=client_secret) and not is_user_registered(vk_id) and timezone <= 14 and timezone >= -12:
        user = Vkuser(id_vk=vk_id, common=costsPattern,
                      fun=costsPattern, invest=costsPattern, register_date=register_date, timezone=timezone)
        user.save()

        response['RESPONSE'] = 'SIGN_UP_SUCCESS'
        response['PAYLOAD'] = {}
        response['PAYLOAD']['vk_id'] = vk_id
        # response['PAYLOAD']['name'] = name
        # response['PAYLOAD']['sure_name'] = sure_name
        response['PAYLOAD']['is_tutorial_done'] = False
        with_time_zone = register_date + timedelta(hours=timezone)

        response['PAYLOAD']['register_date'] = with_time_zone
        response['PAYLOAD']['is_vk_theme'] = True
        response['PAYLOAD']['is_costom_dark_theme'] = False

        print('[sign_up_by_vk_id:RESPONSE]-->', response)
        return JsonResponse(response)
    else:
        print('[sign_up_by_vk_id:RESPONSE]-->', response)
        return JsonResponse(response)
