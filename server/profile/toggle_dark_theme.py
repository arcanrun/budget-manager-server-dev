import json
from django.http import JsonResponse
import datetime
from ..models import Vkuser, History

from ..helpers import logger, get_updated_data, make_calculations, make_calculations_full,  costsPattern, history_saver, next_pay_day, get_id_from_vk_params, is_user_registered

from ..auth.chcek_sign import is_valid, insert_client_sign, make_dict_from_query


def toggle_dark_theme(request):
    response = {'RESPONSE': 'ERROR_AUTH', 'PAYLOAD': 'ERROR'}
    req = json.loads(str(request.body, encoding='utf-8'))
    logger('toggle_dark_theme:RECIVED-->', req)

    is_costom_dark_theme = req['is_costom_dark_theme']
    vk_id = get_id_from_vk_params(str(req['params']))
    query_params = make_dict_from_query(str(req['params']))
    client_secret = insert_client_sign()

    if is_valid(query=query_params, secret=client_secret) and type(is_costom_dark_theme) is bool:
        all_users = Vkuser.objects.all()
        for field in all_users:
            if (vk_id == field.id_vk):
                Vkuser.objects.filter(id_vk=vk_id).update(
                    is_costom_dark_theme=is_costom_dark_theme)
                break
        response["RESPONSE"] = 'SUCCESS'
        response["PAYLOAD"] = {'is_costom_dark_theme': is_costom_dark_theme}

        logger('toggle_dark_theme:RESPONSE-->', response)
        return JsonResponse(response)
    else:
        logger('toggle_dark_theme:RESPONSE-->', response)
        return JsonResponse(response)
