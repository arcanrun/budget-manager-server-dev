"""
This is Calendar logic

When user hits the date on the calandar and press the 'yes' button the rest of the magic happens here

It is used for first entry and for other changes
"""

import json
import datetime
from django.http import JsonResponse
from ..models import Vkuser, History

from ..helpers import get_updated_data, make_calculations, make_calculations_full,  costsPattern, history_saver, next_pay_day, get_id_from_vk_params, is_user_registered

from ..auth.chcek_sign import is_valid, insert_client_sign, make_dict_from_query


def set_new_pay_date(request):
    req = json.loads(str(request.body, encoding='utf-8'))
    print('[set_new_pay_date:RECIVED]-->', req)
    response = {'RESPONSE': 'AUTH_ERROR_OR_BAD_QUERY', 'PAYLOAD': {}}
    pay_day = str(req['payday'])
    to_day = str(req['toDay'])
    vk_id = get_id_from_vk_params(str(req['params']))
    query_params = make_dict_from_query(str(req['params']))
    client_secret = insert_client_sign()
    if is_valid(query=query_params, secret=client_secret) and (pay_day >= to_day or next_pay_day(pay_day) == next_pay_day(to_day)):

        all_users = Vkuser.objects.all()

        for field in all_users:
            if (vk_id == field.id_vk):
                new_days_to_payday = next_pay_day(
                    pay_day) - next_pay_day(to_day)
                new_days_to_payday = new_days_to_payday.days
                resArr = make_calculations_full(
                    field.common, field.fun, field.invest, new_days_to_payday,  field.budget)

                Vkuser.objects.filter(id_vk=vk_id).update(
                    pay_day=pay_day, days_to_payday=new_days_to_payday, common=resArr[0], fun=resArr[1], invest=resArr[2])
                break

        response = get_updated_data(vk_id)
        print('[set_new_pay_date:RESPONSE]-->', response)

        return JsonResponse(response)
    else:
        print('[set_new_pay_date:RESPONSE]-->', response)

        return JsonResponse(response)
