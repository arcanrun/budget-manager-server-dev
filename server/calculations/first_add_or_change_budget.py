"""
1.'ADD' ==> First adding budget - when user make first entry
2. 'CHANGE' ==> Changing the budegt - when user hits the 'PEN' icon

"""
import json
from django.http import JsonResponse
from ..models import Vkuser, History

from ..helpers import is_valid_number, get_updated_data, make_calculations, make_calculations_full,  costsPattern, history_saver, next_pay_day, get_id_from_vk_params, is_user_registered

from ..auth.chcek_sign import is_valid, insert_client_sign, make_dict_from_query


def first_add_or_change_budget(request):
    req = json.loads(str(request.body, encoding='utf-8'))
    print('[first_add_or_change_budget:RECIVED]-->', req)
    vk_id = get_id_from_vk_params(str(req['params']))
    query_params = make_dict_from_query(str(req['params']))
    client_secret = insert_client_sign()

    response = {'RESPONSE': 'AUTH_ERROR', 'PAYLOAD': {}}

    if is_valid(query=query_params, secret=client_secret):
        if not is_valid_number(req['budget']):
            response = {'RESPONSE': 'VALUE_ERROR', 'PAYLOAD': {}}
            return JsonResponse(response)
        budget = round(float(req['budget']), 2)
        operation = str(req['operation'])

        all_users = Vkuser.objects.all()
        # ADD - add the value for first time, when user make firt entry
        if operation == 'add':

            for field in all_users:
                if (vk_id == field.id_vk):
                    Vkuser.objects.filter(id_vk=vk_id).update(
                        budget=budget)
                    break
            response = get_updated_data(vk_id)
            print('[ADD__first_add_or_change_budget:RESPONSE]-->', response)
            return JsonResponse(response)

        if operation == 'change':
            for field in all_users:
                if (vk_id == field.id_vk):

                    resArr = make_calculations_full(
                        field.common, field.fun, field.invest, field.days_to_payday, budget)
                    Vkuser.objects.filter(id_vk=vk_id).update(
                        budget=budget, common=resArr[0], fun=resArr[1], invest=resArr[2])
                    break
            response = get_updated_data(vk_id)
            response['TEST'] = resArr
            print('[CHANGE__first_add_or_change_budget:RESPONSE]-->', response)

            return JsonResponse(response)
    else:
        print('[first_add_or_change_budget:RESPONSE]-->', response)

        return JsonResponse(response)
