import json
import datetime
from datetime import timedelta
from django.utils import timezone

from django.http import JsonResponse
from ..models import Vkuser, History
from ..helpers import is_valid_number, logger, get_updated_data, make_calculations, make_calculations_full,  costsPattern, history_saver, next_pay_day, get_id_from_vk_params, is_user_registered

from ..auth.chcek_sign import is_valid, insert_client_sign, make_dict_from_query

currency_map = ['USD', 'RUB', 'YEN']


def get_enter_data(request):
    req = json.loads(str(request.body, encoding='utf-8'))
    response = {'RESPONSE': 'SIGN_UP_ERROR_OR_BAD_REQUEST', 'PAYLOAD': False}

    vk_id = get_id_from_vk_params(str(req['params']))
    query_params = make_dict_from_query(str(req['params']))
    client_secret = insert_client_sign()

    currency = str(req['currency']).upper()
    pay_day = str(req['payday'])

    logger('get_enter_data:RECIVED', req)

    try:
        pay_day = datetime.datetime.strptime(
            pay_day, "%Y-%m-%dT%H:%M:%S.%fZ")
    except:
        response = {'RESPONSE': 'VALUE_ERROR', 'PAYLOAD': {}}
        return JsonResponse(response)

    if is_valid(query=query_params, secret=client_secret) and len(currency) == 3 and currency in currency_map:
        if not is_valid_number(req['budget']):
            response = {'RESPONSE': 'VALUE_ERROR', 'PAYLOAD': {}}
            return JsonResponse(response)
        budget = round(float(req['budget']), 2)

        response = {'PAYLOAD': 'ALL GOOD'}
        return JsonResponse(response)
    else:
        return JsonResponse(response)
