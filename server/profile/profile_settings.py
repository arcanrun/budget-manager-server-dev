import json
from django.http import JsonResponse
import datetime
from datetime import timedelta
from ..models import Vkuser, History

from ..helpers import logger, get_updated_data, make_calculations, make_calculations_full,  costsPattern, history_saver, next_pay_day, get_id_from_vk_params, is_user_registered

from ..auth.chcek_sign import is_valid, insert_client_sign, make_dict_from_query


def profile_settings(request):
    response = {'RESPONSE': 'ERROR_AUTH', 'PAYLOAD': 'ERROR'}
    req = json.loads(str(request.body, encoding='utf-8'))
    logger('profile_manage:RECIVED-->', req)

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
        logger('profile_manage:RESPONSE-->', response)

        if operation == 'history_delete_all':
            for field in history:
                if (vk_id == field.id_vk):
                    History.objects.filter(id_vk=vk_id).delete()
            response = {'RESPONSE': 'HISTORY_DELETE_ALL',
                        'PAYLOAD': vk_id}
        logger('profile_manage:RESPONSE-->', response)

        if operation == 'toggle_full_history':
            for field in all_users:
                if(vk_id == field.id_vk):
                    Vkuser.objects.filter(id_vk=vk_id).update(
                        is_full_history=not field.is_full_history)
            response = {'RESPONSE': 'TOGGLE_IS_FULL_HISTORY',
                        'PAYLOAD': not field.is_full_history}
        logger('profile_manage:RESPONSE-->', response)

        if operation == 'history_delete_month':
            req_month = str(req['payload'])
            response = {'RESPONSE': 'ERROR_AUTH', 'PAYLOAD': 'ERROR'}
            try:
                foramated_date = ''
                for field in all_users:
                    if(vk_id == field.id_vk):
                        timezone = field.timezone
                        with_time_zone = datetime.datetime.strptime(
                            req_month, '%Y-%m-%dT%H:%M:%S.%fZ') + timedelta(hours=timezone)
                        foramated_date = with_time_zone.strftime('%m')
                        break
                for field in history:
                    if(vk_id == field.id_vk):
                        date = datetime.datetime.strptime(
                            field.date, '%Y-%m-%d %H:%M:%S.%f')
                        date = date.strftime('%m')
                        if date == foramated_date:
                            print('------------>', field.id)
                            History.objects.filter(id=field.id).delete()

                response = {'RESPONSE': 'MONTH_CLEARD', 'PAYLOAD': 'SUCCESS'}

            except Exception:
                response = {'RESPONSE': 'ERROR_AUTH', 'PAYLOAD': 'ERROR'}

            # for field in history:
            #     if (vk_id == field.id_vk and month == ???):
            #         History.objects.filter(id_vk=vk_id).delete()
            # response = {'RESPONSE': 'HISTORY_DELETE_ALL',
            #             'PAYLOAD': vk_id}
        logger('profile_manage:RESPONSE-->', response)

        return JsonResponse(response)
    else:
        logger('profile_manage:RESPONSE-->', response)
        return JsonResponse(response)
