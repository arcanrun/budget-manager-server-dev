"""
This is Calendar logic

When user hits the date on the calandar and press the 'yes' button the rest of the magic happens here 

It is used for first entry and for other changes 
"""

import json
from django.http import JsonResponse
from ..models import Vkuser, History

from ..helpers import get_updated_data, make_calculations, make_calculations_full,  costsPattern, history_saver, next_pay_day


def set_new_pay_date(request):
    req = json.loads(str(request.body, encoding='utf-8'))
    print('[set_new_pay_date:RECIVED]-->', req)
    response = {'RESPONSE': 'ERROR', 'PAYLOAD': {}}

    vk_id = str(req['vk_id'])
    pay_day = str(req['payday'])
    days_to_payday = int(req['days_to_payday'])

    all_users = Vkuser.objects.all()

    for field in all_users:
        if (vk_id == field.id_vk):

            resArr = make_calculations_full(
                field.common, field.fun, field.invest, days_to_payday,  field.budget)

            Vkuser.objects.filter(id_vk=vk_id).update(
                pay_day=pay_day, days_to_payday=days_to_payday, common=resArr[0], fun=resArr[1], invest=resArr[2])
            break

    response = get_updated_data(vk_id)
    response['TEST'] = resArr
    print('[set_new_pay_date:RESPONSE]-->', response)

    return JsonResponse(response)
