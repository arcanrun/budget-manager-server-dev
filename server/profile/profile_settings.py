import json
from django.http import JsonResponse
import datetime
from ..models import Vkuser, History

from ..helpers import get_updated_data, make_calculations, make_calculations_full,  costsPattern, history_saver, next_pay_day, get_id_from_vk_params, is_user_registered

from ..auth.chcek_sign import is_valid, insert_client_sign, make_dict_from_query


def profile_settings(request):
    response = {'RESPONSE': 'ERROR_AUTH', 'PAYLOAD': 'ERROR'}
    req = json.loads(str(request.body, encoding='utf-8'))
    print('[profile_manage:RECIVED]-->', req)

    operation = req['operationType']
    vk_id = get_id_from_vk_params(str(req['params']))
    query_params = make_dict_from_query(str(req['params']))
    client_secret = insert_client_sign()

    if is_valid(query=query_params, secret=client_secret):
        all_users = Vkuser.objects.all()
        history = History.objects.all()

        if operation == 'delete':
            for field in all_users:
                if (vk_id == field.id_vk):
                    Vkuser.objects.filter(id_vk=vk_id).delete()
            for field in history:
                if (vk_id == field.id_vk):
                    History.objects.filter(id_vk=vk_id).delete()
            response = {'RESPONSE': 'DELETE_USER_SUCCESS',
                        'PAYLOAD': vk_id}
        print('[profile_manage:RESPONSE]-->', response)
        return JsonResponse(response)
    else:
        print('[profile_manage:RESPONSE]-->', response)
        return JsonResponse(response)
