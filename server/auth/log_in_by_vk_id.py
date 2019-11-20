import json

import datetime
from datetime import timedelta
from django.utils import timezone


from urllib.parse import urlparse, parse_qsl, urlencode

from django.http import JsonResponse
from ..models import Vkuser, History

from ..helpers import get_updated_data, make_calculations, make_calculations_full,  costsPattern, history_saver, next_pay_day, get_id_from_vk_params, is_user_registered

from ..auth.chcek_sign import is_valid, insert_client_sign, make_dict_from_query
from .check_origin import is_allowed_origin


def log_in_by_vk_id(request):
    if not is_allowed_origin(request):
        return JsonResponse({
            'RESPONSE': 'BAD_REQUEST'
        })

    req = json.loads(str(request.body, encoding='utf-8'))
    print('[log_in_by_vk_id:RECIVED]-->', req)

    vk_id = get_id_from_vk_params(str(req['params']))
    query_params = make_dict_from_query(str(req['params']))
    timezone = int(req['timezone'])
    client_secret = insert_client_sign()

    response = {'RESPONSE': 'LOGIN_ERROR', 'PAYLOAD': {}}

    if is_valid(query=query_params, secret=client_secret) and timezone <= 14 and timezone >= -12:
        all_users = Vkuser.objects.all()
        for field in all_users:
            if (vk_id == field.id_vk):
                response['RESPONSE'] = 'LOG_IN'
                response['PAYLOAD']['vk_id'] = field.id_vk
                response['PAYLOAD']['name'] = field.name
                response['PAYLOAD']['sure_name'] = field.sure_name
                response['PAYLOAD']['is_tutorial_done'] = field.is_tutorial_done
                response['PAYLOAD']['is_vk_theme'] = field.is_vk_theme
                response['PAYLOAD']['is_costom_dark_theme'] = field.is_costom_dark_theme

                with_time_zone = datetime.datetime.strptime(
                    field.register_date, '%Y-%m-%d %H:%M:%S.%f') + timedelta(hours=field.timezone)

                response['PAYLOAD']['register_date'] = with_time_zone
                if field.timezone != timezone:
                    print(type(field.timezone), type(timezone))
                    Vkuser.objects.filter(id_vk=vk_id).update(
                        timezone=timezone)
        print('[log_in_by_vk_id:RESPONSE]-->', response)
        return JsonResponse(response)

    print('[log_in_by_vk_id:RESPONSE]-->', response)
    return JsonResponse(response)
