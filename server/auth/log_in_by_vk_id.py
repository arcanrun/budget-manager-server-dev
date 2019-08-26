import json
from django.http import JsonResponse
from ..models import Vkuser, History

from ..helpers import get_updated_data, make_calculations, make_calculations_full,  costsPattern, history_saver, next_pay_day


def log_in_by_vk_id(request):
    req = json.loads(str(request.body, encoding='utf-8'))
    print('[log_in_by_vk_id:RECIVED]-->', req)

    vk_id = str(req['vk_id'])
    name = str(req['name'])
    sure_name = str(req['sure_name'])
    avatar = str(req['avatar'])

    response = {'RESPONSE': 'LOGIN_ERROR', 'PAYLOAD': {}
                }

    all_users = Vkuser.objects.all()
    for field in all_users:
        if (vk_id == field.id_vk):
            response['RESPONSE'] = 'ALREADY_HERE'
            response['PAYLOAD']['vk_id'] = field.id_vk
            response['PAYLOAD']['name'] = name
            response['PAYLOAD']['sure_name'] = sure_name
            response['PAYLOAD']['avatar'] = avatar
            # response['PAYLOAD']['is_tutorial_done'] = field.is_tutorial_done

            print('[log_in_by_vk_id:RESPONSE]-->', response)
            return JsonResponse(response)

    # user = Vkuser(id_vk=vk_id, common=costsPattern,
    #               fun=costsPattern, invest=costsPattern)
    # user.save()

    print('[log_in_by_vk_id:RESPONSE]-->', response)

    return JsonResponse(response)
