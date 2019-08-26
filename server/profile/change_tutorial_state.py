import json
from django.http import JsonResponse
import datetime
from ..models import Vkuser, History

from ..helpers import get_updated_data, make_calculations, make_calculations_full,  costsPattern, history_saver, next_pay_day


def change_tutorial_state(request):
    response = {'RESPONSE': 'ERROR', 'PAYLOAD': 'ERROR'}
    req = json.loads(str(request.body, encoding='utf-8'))
    print('[change_tutorial_state:RECIVED]-->', req)

    vk_id = str(req['vk_id'])
    is_tutorial_done = str(req['is_tutorial_done'])
    all_users = Vkuser.objects.all()
    for field in all_users:
        if (vk_id == field.id_vk):
            Vkuser.objects.filter(id_vk=vk_id).update(
                is_tutorial_done=is_tutorial_done)
            break

    print('[log_in_by_vk_id:RESPONSE]-->', response)
    return JsonResponse(response)
