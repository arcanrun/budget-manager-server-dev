import json
import datetime
from datetime import timedelta
from django.utils import timezone

from django.http import JsonResponse
from ..models import Vkuser, History
from ..helpers import is_valid_number, logger, get_updated_data, make_calculations, make_calculations_full,  costsPattern, history_saver, next_pay_day, get_id_from_vk_params, is_user_registered

from ..auth.chcek_sign import is_valid, insert_client_sign, make_dict_from_query

currency_map = [
      "AED",
      "AFN",
      "ALL",
      "AMD",
      "ANG",
      "AOA",
      "ARS",
      "AUD",
      "AWG",
      "AZN",
      "BAM",
      "BBD",
      "BDT",
      "BGN",
      "BHD",
      "BIF",
      "BMD",
      "BND",
      "BOB",
      "BRL",
      "BSD",
      "BTC",
      "BTN",
      "BWP",
      "BYR",
      "BYN",
      "BZD",
      "CAD",
      "CDF",
      "CHF",
      "CLP",
      "CNY",
      "COP",
      "CRC",
      "CUC",
      "CUP",
      "CVE",
      "CZK",
      "DJF",
      "DKK",
      "DOP",
      "DZD",
      "EEK",
      "EGP",
      "ERN",
      "ETB",
      "ETH",
      "EUR",
      "FJD",
      "FKP",
      "GBP",
      "GEL",
      "GGP",
      "GHC",
      "GHS",
      "GIP",
      "GMD",
      "GNF",
      "GTQ",
      "GYD",
      "HKD",
      "HNL",
      "HRK",
      "HTG",
      "HUF",
      "IDR",
      "ILS",
      "IMP",
      "INR",
      "IQD",
      "IRR",
      "ISK",
      "JEP",
      "JMD",
      "JOD",
      "JPY",
      "KES",
      "KGS",
      "KHR",
      "KMF",
      "KPW",
      "KRW",
      "KWD",
      "KYD",
      "KZT",
      "LAK",
      "LBP",
      "LKR",
      "LRD",
      "LSL",
      "LTC",
      "LTL",
      "LVL",
      "LYD",
      "MAD",
      "MDL",
      "MGA",
      "MKD",
      "MMK",
      "MNT",
      "MOP",
      "MRO",
      "MRU",
      "MUR",
      "MVR",
      "MWK",
      "MXN",
      "MYR",
      "MZN",
      "NAD",
      "NGN",
      "NIO",
      "NOK",
      "NPR",
      "NZD",
      "OMR",
      "PAB",
      "PEN",
      "PGK",
      "PHP",
      "PKR",
      "PLN",
      "PYG",
      "QAR",
      "RMB",
      "RON",
      "RSD",
      "RUB",
      "RWF",
      "SAR",
      "SBD",
      "SCR",
      "SDG",
      "SEK",
      "SGD",
      "SHP",
      "SLL",
      "SOS",
      "SRD",
      "SSP",
      "STD",
      "STN",
      "SVC",
      "SYP",
      "SZL",
      "THB",
      "TJS",
      "TMT",
      "TND",
      "TOP",
      "TRL",
      "TRY",
      "TTD",
      "TVD",
      "TWD",
      "TZS",
      "UAH",
      "UGX",
      "USD",
      "UYU",
      "UZS",
      "VEF",
      "VND",
      "VUV",
      "WST",
      "XAF",
      "XBT",
      "XCD",
      "XOF",
      "XPF",
      "YER",
      "ZAR",
      "ZWD"
    ]


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
        datetime.datetime.strptime(
            pay_day, "%Y-%m-%dT%H:%M:%S.%fZ")
        print('1----', pay_day)

    except:
        response = {'RESPONSE': 'VALUE_ERROR', 'PAYLOAD': {}}
        print('2----', pay_day)
        return JsonResponse(response)

    print('3----')

    if is_valid(query=query_params, secret=client_secret) and len(currency) == 3 and currency in currency_map:

        if not is_valid_number(req['budget']):
            response = {'RESPONSE': 'VALUE_ERROR', 'PAYLOAD': {}}
            return JsonResponse(response)
        budget = round(float(req['budget']), 2)

        all_users = Vkuser.objects.all()
        for field in all_users:

            if (vk_id == field.id_vk):

                pay_day = datetime.datetime.strptime(
                    str(pay_day), "%Y-%m-%dT%H:%M:%S.%fZ") + timedelta(hours=field.timezone)

                to_day = datetime.datetime.now() + timedelta(hours=field.timezone)

                to_day_with_timezone = to_day + timedelta(hours=field.timezone)

                to_day_with_timezone = datetime.date.strftime(
                    to_day_with_timezone, '%Y-%m-%d')

                to_day_with_timezone = datetime.datetime.strptime(
                    to_day_with_timezone, '%Y-%m-%d')

                pay_day = datetime.date.strftime(
                    pay_day, '%Y-%m-%d')

                pay_day = datetime.datetime.strptime(
                    pay_day, '%Y-%m-%d')

                new_days_to_payday = pay_day - to_day_with_timezone
                new_days_to_payday = new_days_to_payday.days

                if(new_days_to_payday < 0):
                    return JsonResponse({"RESPONSE": "BAD_REQUEST"})
                resArr = make_calculations_full(
                    field.common, field.fun, field.invest, new_days_to_payday, budget)

                Vkuser.objects.filter(id_vk=vk_id).update(
                    pay_day=pay_day, days_to_payday=new_days_to_payday, common=resArr[0], fun=resArr[1], invest=resArr[2], budget=budget, currency=currency)

                break
        response = get_updated_data(vk_id)

        logger('get_enter_data:RESPONSE', response)

        return JsonResponse(response)
    else:
        return JsonResponse(response)
