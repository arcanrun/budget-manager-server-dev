"""
Used for history page
"""
import json
from django.http import JsonResponse
import datetime
from datetime import timedelta
from ..models import Vkuser, History

from ..helpers import logger, get_updated_data, make_calculations, make_calculations_full,  costsPattern, history_saver, next_pay_day, get_id_from_vk_params, is_user_registered

from ..auth.chcek_sign import is_valid, insert_client_sign, make_dict_from_query


def get_history(request):
    response = {'RESPONSE': 'ERROR_AUTH', 'PAYLOAD': []}
    req = json.loads(str(request.body, encoding='utf-8'))
    logger('get_history:RECIVED', req)

    vk_id = get_id_from_vk_params(str(req['params']))
    query_params = make_dict_from_query(str(req['params']))
    client_secret = insert_client_sign()

    if is_valid(query=query_params, secret=client_secret):
        history = History.objects.all()
        user = Vkuser.objects.all()
        history_object = {}
        cost_object = {'type_cost': '', 'operation': '', 'value': '', 'id': ''}
        timezone = ''
        is_full_history = True

        for user_field in user:
            if (vk_id == user_field.id_vk):
                timezone = user_field.timezone
                is_full_history = user_field.is_full_history
                break
        for field in history:

            if (vk_id == field.id_vk):
                if not is_full_history:
                    with_time_zone = datetime.datetime.strptime(
                        field.date, '%Y-%m-%d %H:%M:%S.%f') + timedelta(hours=timezone)
                    foramated_date = with_time_zone.strftime('%Y-%m-%d')
                    # foramated_date = datetime.datetime.strptime(
                    #     foramated_date, '%Y-%m-%d')
                    # foramated_date = foramated_date.strftime('%d.%m.%Y')

                    # if date presents in history_object:
                    curent_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                    current_date_timezone = datetime.datetime.strptime(
                        curent_date, '%Y-%m-%d %H:%M:%S.%f') + timedelta(hours=timezone)
                    current_date_formated = current_date_timezone.strftime(
                        '%Y-%m')
                    foramated_date_month = with_time_zone.strftime('%Y-%m')

                    if current_date_formated == foramated_date_month:
                        if foramated_date in history_object:
                            cost_object['type_cost'] = field.type_costs
                            cost_object['value'] = field.value
                            cost_object['operation'] = field.operation
                            cost_object['id'] = field.id
                            cost_object['comment'] = field.comment

                        # if date doesn't present in history_object then make new one:
                        else:
                            history_object[foramated_date] = []

                            cost_object['type_cost'] = field.type_costs
                            cost_object['value'] = field.value
                            cost_object['operation'] = field.operation
                            cost_object['id'] = field.id
                            cost_object['comment'] = field.comment

                        history_object[foramated_date].append(cost_object)

                        cost_object = {'type_cost': '',
                                       'operation': '', 'value': '', 'id': ''}

                else:
                    with_time_zone = datetime.datetime.strptime(
                        field.date, '%Y-%m-%d %H:%M:%S.%f') + timedelta(hours=timezone)
                    foramated_date = with_time_zone.strftime('%Y-%m-%d')

                    if foramated_date in history_object:
                        cost_object['type_cost'] = field.type_costs
                        cost_object['value'] = field.value
                        cost_object['operation'] = field.operation
                        cost_object['id'] = field.id
                        cost_object['comment'] = field.comment

                    # if date doesn't present in history_object then make new one:
                    else:
                        history_object[foramated_date] = []

                        cost_object['type_cost'] = field.type_costs
                        cost_object['value'] = field.value
                        cost_object['operation'] = field.operation
                        cost_object['id'] = field.id
                        cost_object['comment'] = field.comment

                    history_object[foramated_date].append(cost_object)

                    cost_object = {'type_cost': '',
                                   'operation': '', 'value': '', 'id': ''}

        for k, v in history_object.items():
            v.reverse()
            response['PAYLOAD'].append({k: v})
        response['PAYLOAD'].reverse()
        response['RESPONSE'] = 'SUCCESS'

        logger('get_history:RESPONSE', response)

        return JsonResponse(response)

    else:
        logger('get_history:RESPONSE', response)

        return JsonResponse(response)
