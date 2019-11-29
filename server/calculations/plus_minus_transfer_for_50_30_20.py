"""
All calcs for 50 or 30 or 20 budget and also the max for to day

Transfer goes here too!
"""
import json
from django.http import JsonResponse
from ..models import Vkuser, History
from ..helpers import is_comment_valid, clear_string, logger, is_valid_number, get_updated_data, make_calculations, make_calculations_full,  costsPattern, history_saver, next_pay_day, get_id_from_vk_params, is_user_registered
import datetime

from ..auth.chcek_sign import is_valid, insert_client_sign, make_dict_from_query


def plus_minus_transfer_for_50_30_20(request):
    req = json.loads(str(request.body, encoding='utf-8'))

    logger('plus_minus_transfer_for_50_30_20:RECIVED', req)

    try:
        comment = clear_string(req['comment'])
        if not is_comment_valid(comment):
            return JsonResponse({
                'RESPONSE': 'BAD_REQUEST'
            })
    except:
        comment = False

    vk_id = get_id_from_vk_params(str(req['params']))
    query_params = make_dict_from_query(str(req['params']))
    client_secret = insert_client_sign()

    if is_valid(query=query_params, secret=client_secret):
        if not is_valid_number(req['value']):
            response = {'RESPONSE': 'VALUE_ERROR', 'PAYLOAD': {}}
            return JsonResponse(response)
        typeCost = req['type']
        value = round(float(req['value']), 2)
        operation = req['operation']
        # date_now = req['date_now']
        date_now = datetime.datetime.now()
        newBudget = ''
        costsObject = {}
        all_users = Vkuser.objects.all()
        for field in all_users:
            if (vk_id == field.id_vk):
                # from json to dict
                costsObject["common"] = json.loads(field.common)
                costsObject["fun"] = json.loads(field.fun)
                costsObject["invest"] = json.loads(field.invest)

                # if not 'tempMonth' in costsObject['common']:
                #     costsObject["common"]["tempMonth"] = costsObject["common"]["value"]
                #     costsObject["fun"]["tempMonth"] = costsObject["fun"]["value"]
                #     costsObject["invest"]["tempMonth"] = costsObject["invest"]["value"]

                if operation == 'plus':

                    newBudget = float(field.budget) + value

                    costsObject[typeCost]['temp'] = round(
                        costsObject[typeCost]['temp'] + value, 2)

                    costsObject[typeCost]['tempMonth'] = round(
                        costsObject[typeCost]['tempMonth'] + value, 2)

                    if (costsObject[typeCost]['temp'] > costsObject[typeCost]['maxToday']):
                        costsObject[typeCost]['maxToday'] = costsObject[typeCost]['temp']

                    if (costsObject[typeCost]['tempMonth'] > costsObject[typeCost]['value']):
                        costsObject[typeCost]['value'] = costsObject[typeCost]['tempMonth']

                    # from dict to json
                    costsObject['common'] = json.dumps(costsObject['common'])
                    costsObject['fun'] = json.dumps(costsObject['fun'])
                    costsObject['invest'] = json.dumps(costsObject['invest'])

                if operation == 'minus':
                    res = costsObject[typeCost]['tempMonth'] = round(
                        costsObject[typeCost]['tempMonth'] - value, 2)

                    newBudget = float(field.budget) - value

                    if newBudget <= 0:
                        resArr = make_calculations_full(
                            field.common, field.fun, field.invest, field.days_to_payday, newBudget)

                        costsObject['common'] = resArr[0]
                        costsObject['fun'] = resArr[1]
                        costsObject['invest'] = resArr[2]
                    else:
                        costsObject[typeCost]['tempMonth'] = res
                        costsObject[typeCost]['temp'] = round(
                            costsObject[typeCost]['temp'] - value, 2)

                        # from dict to json
                        costsObject['common'] = json.dumps(
                            costsObject['common'])
                        costsObject['fun'] = json.dumps(costsObject['fun'])
                        costsObject['invest'] = json.dumps(
                            costsObject['invest'])

                if operation == 'transfer':
                    transfer_to = str(req['transfer_to'])

                    costsObject[typeCost]['value'] = round(
                        costsObject[typeCost]['value'] - value, 2)

                    costsObject[transfer_to]['value'] = round(
                        costsObject[transfer_to]['value'] + value, 2)

                    calc = make_calculations(
                        json.dumps(costsObject["common"]),  json.dumps(costsObject["fun"]),  json.dumps(costsObject["invest"]), field.days_to_payday, field.budget)

                    costsObject['common'] = calc[0]
                    costsObject['fun'] = calc[1]
                    costsObject['invest'] = calc[2]
                    newBudget = float(field.budget)
                    print('===============>', costsObject)

                history_saver(field.id_vk, date_now,
                              operation, value, typeCost, comment)
                Vkuser.objects.filter(id_vk=vk_id).update(
                    budget=round(newBudget, 2), common=costsObject["common"], fun=costsObject["fun"], invest=costsObject["invest"])
                break

        response = get_updated_data(vk_id)
        logger('plus_minus_transfer_for_50_30_20:RESPONSE', response)

        return JsonResponse(response)
    else:
        response = {'RESPONSE': 'AUTH_ERROR', 'PAYLOAD': {}}
        logger('plus_minus_transfer_for_50_30_20:RESPONSE', response)

        return JsonResponse(response)
