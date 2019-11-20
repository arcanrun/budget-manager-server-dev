import json
from django.http import JsonResponse
import datetime
from ..models import Vkuser, History

from ..helpers import logger, get_updated_data, make_calculations, make_calculations_full,  costsPattern, history_saver, next_pay_day, get_id_from_vk_params, is_user_registered

from ..auth.chcek_sign import is_valid, insert_client_sign, make_dict_from_query


def change_tutorial_state(request):
    response = {'RESPONSE': 'AUTH_ERROR', 'PAYLOAD': ''}
    req = json.loads(str(request.body, encoding='utf-8'))
    logger('change_tutorial_state:RECIVED-->', req)

    vk_id = get_id_from_vk_params(str(req['params']))
    query_params = make_dict_from_query(str(req['params']))
    client_secret = insert_client_sign()
    is_tutorial_done = req['is_tutorial_done']
    if is_valid(query=query_params, secret=client_secret) and type(is_tutorial_done) is bool:
        all_users = Vkuser.objects.all()
        for field in all_users:
            if (vk_id == field.id_vk):
                Vkuser.objects.filter(id_vk=vk_id).update(
                    is_tutorial_done=is_tutorial_done)
                break
        response["RESPONSE"] = 'SUCCESS'
        response["PAYLOAD"] = {'is_tutorial_done': is_tutorial_done}

        logger('change_tutorial_state:RESPONSE-->', response)
        return JsonResponse(response)
    else:
        logger('change_tutorial_state:RESPONSE-->', response)
        return JsonResponse(response)
