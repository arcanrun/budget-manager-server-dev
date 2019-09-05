import json
from django.http import JsonResponse
from ..models import Vkuser, History

from ..helpers import get_updated_data, make_calculations, make_calculations_full,  costsPattern, history_saver, next_pay_day, get_id_from_vk_params, is_user_registered

from ..auth.chcek_sign import is_valid, insert_client_sign, make_dict_from_query


def get_stat_for_current_month(request):
    response = {'RESPONSE': 'ERROR', 'PAYLOAD': {}}
    req = json.loads(str(request.body, encoding='utf-8'))
    print('[get_stat_for_current_month:RECIVED]-->', req)

    vk_id = get_id_from_vk_params(str(req['params']))
    query_params = make_dict_from_query(str(req['params']))
    client_secret = insert_client_sign()

    if is_valid(query=query_params, secret=client_secret):
        toDayMonth = req['toDayFormated'][3:]
        costs = {
            'total': 0,
            'common': 0,
            'fun': 0,
            'invest': 0,
        }
        income = {
            'total': 0,
            'common': 0,
            'fun': 0,
            'invest': 0,
        }

        history = History.objects.all()
        for field in history:
            if (vk_id == field.id_vk and field.date[3:] == toDayMonth):
                if field.operation == 'minus':
                    costs['total'] += float(field.value)
                    if field.type_costs == 'common':
                        costs['common'] += float(field.value)
                    if field.type_costs == 'fun':
                        costs['fun'] += float(field.value)
                    if field.type_costs == 'invest':
                        costs['invest'] += float(field.value)
                if field.operation == 'plus':
                    income['total'] += float(field.value)
                    if field.type_costs == 'common':
                        income['common'] += float(field.value)
                    if field.type_costs == 'fun':
                        income['fun'] += float(field.value)
                    if field.type_costs == 'invest':
                        income['invest'] += float(field.value)
        response['RESPONSE'] = 'FETCHED_STATISTICS_SUCCESS'
        response['PAYLOAD']['costs'] = costs
        response['PAYLOAD']['income'] = income

        print('[get_stat_for_current_month:RESPONSE]-->', response)
        return JsonResponse(response)
    else:
        print('[get_stat_for_current_month:RESPONSE]-->', response)
        return JsonResponse(response)
