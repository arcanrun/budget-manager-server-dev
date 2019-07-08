"""
All calcs for 50 or 30 or 20 budget and also the max for to day

Transfer goes here too!
"""
import json
from django.http import JsonResponse
from ..models import Vkuser, History
from ..helpers import get_updated_data, make_calculations, make_calculations_full,  costsPattern, history_saver, next_pay_day


def plus_minus_transfer_for_50_30_20(request):
    req = json.loads(str(request.body, encoding='utf-8'))
    print('[temp_today_cost:RECIVED]-->', req)

    vk_id = str(req['vk_id'])
    typeCost = req['type']
    value = round(float(req['value']), 2)
    operation = req['operation']
    date_now = req['date_now']
    newBudget = ''
    costsObject = {}
    all_users = Vkuser.objects.all()
    for field in all_users:
        if (vk_id == field.id_vk):

            costsObject["common"] = json.loads(field.common)
            costsObject["fun"] = json.loads(field.fun)
            costsObject["invest"] = json.loads(field.invest)

            if operation == 'plus':
                newBudget = float(field.budget) + value
                costsObject[typeCost]['value'] = round(
                    costsObject[typeCost]['value'] + value, 2)
                costsObject[typeCost]['temp'] = round(
                    costsObject[typeCost]['temp'] + value, 2)

                costsObject['common'] = json.dumps(costsObject['common'])
                costsObject['fun'] = json.dumps(costsObject['fun'])
                costsObject['invest'] = json.dumps(costsObject['invest'])

            if operation == 'minus':
                res = costsObject[typeCost]['value'] = round(
                    costsObject[typeCost]['value'] - value, 2)

                if res < 0:
                    if typeCost == 'common' and (costsObject['fun']['value'] - value) > 0 or typeCost == 'invest' and (costsObject['fun']['value'] - value) > 0:
                        costsObject['fun']['value'] = round(
                            costsObject['fun']['value'] - value, 2)
                    elif typeCost == 'common' and (costsObject['fun']['value'] - value) < 0:
                        costsObject['invest']['value'] = round(
                            costsObject['invest']['value'] - value, 2)
                    elif typeCost == 'fun' and (costsObject['common']['value'] - value) > 0:
                        costsObject['common']['value'] = round(
                            costsObject['common']['value'] - value, 2)
                    elif typeCost == 'fun' and (costsObject['common']['value'] - value) < 0:
                        costsObject['invest']['value'] = round(
                            costsObject['invest']['value'] - value, 2)
                    elif typeCost == 'invest' and (costsObject['fun']['value'] - value) < 0:
                        costsObject['common']['value'] = round(
                            costsObject['common']['value'] - value, 2)
                    elif typeCost == 'invest' and (costsObject['fun']['value'] - value) < 0 and (costsObject['common']['value'] - value) < 0:
                        costsObject['fun']['value'] = round(
                            costsObject['fun']['value'] - value, 2)

                newBudget = float(field.budget) - value
                costsObject[typeCost]['value'] = res
                costsObject[typeCost]['temp'] = round(
                    costsObject[typeCost]['temp'] - value, 2)

                costsObject['common'] = json.dumps(costsObject['common'])
                costsObject['fun'] = json.dumps(costsObject['fun'])
                costsObject['invest'] = json.dumps(costsObject['invest'])

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

            history_saver(field.id_vk, date_now, operation, value, typeCost)
            Vkuser.objects.filter(id_vk=vk_id).update(
                budget=round(newBudget, 2), common=costsObject["common"], fun=costsObject["fun"], invest=costsObject["invest"])
            break

    response = get_updated_data(vk_id)
    print('[temp_today_cost:RESPONSE]-->', response)

    return JsonResponse(response)
