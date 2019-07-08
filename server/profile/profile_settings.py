import json
from django.http import JsonResponse
import datetime
from ..models import Vkuser, History

from ..helpers import get_updated_data, make_calculations, make_calculations_full,  costsPattern, history_saver, next_pay_day


def profile_settings(request):
    response = {'RESPONSE': 'ERROR', 'PAYLOAD': 'ERROR'}
    req = json.loads(str(request.body, encoding='utf-8'))
    print('[profile_manage:RECIVED]-->', req)

    vk_id = str(req['vk_id'])
    operation = req['operationType']

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
                    'PAYLOAD': 'DELETE_USER_SUCCESS'}
    print('[profile_manage:RESPONSE]-->', response)
    return JsonResponse(response)
