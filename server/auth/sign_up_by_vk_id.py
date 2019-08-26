import json
from django.http import JsonResponse
from ..models import Vkuser, History
from ..helpers import get_updated_data, make_calculations, make_calculations_full,  costsPattern, history_saver, next_pay_day


def sign_up_by_vk_id(request):
    req = json.loads(str(request.body, encoding='utf-8'))
    response = {'RESPONSE': 'SIGN_UP_ERROR', 'PAYLOAD': False
                }

    vk_id = str(req['vk_id'])
    name = str(req['name'])
    sure_name = str(req['sure_name'])
    avatar = str(req['avatar'])
    register_date = req['toDay']

    print('[sign_up_by_vk_id:RECIVED]-->', req)
    user = Vkuser(id_vk=vk_id, common=costsPattern,
                  fun=costsPattern, invest=costsPattern, register_date=register_date)
    user.save()

    response['RESPONSE'] = 'SIGN_UP_SUCCESS'
    response['PAYLOAD'] = {}
    response['PAYLOAD']['vk_id'] = vk_id
    response['PAYLOAD']['name'] = name
    response['PAYLOAD']['sure_name'] = sure_name
    response['PAYLOAD']['avatar'] = avatar
    response['PAYLODA']['is_tutorial_done'] = False

    print('[sign_up_by_vk_id:RESPONSE]-->', response)
    return JsonResponse(response)
