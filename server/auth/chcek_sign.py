from base64 import b64encode
from collections import OrderedDict
from hashlib import sha256
from hmac import HMAC
from urllib.parse import urlparse, parse_qsl, urlencode


def is_valid(*, query: dict, secret: str) -> bool:
    """Check VK Apps signature"""
    vk_subset = OrderedDict(
        sorted(x for x in query.items() if x[0][:3] == "vk_"))
    hash_code = b64encode(HMAC(secret.encode(), urlencode(
        vk_subset, doseq=True).encode(), sha256).digest())
    decoded_hash_code = hash_code.decode(
        'utf-8')[:-1].replace('+', '-').replace('/', '_')
    return query["sign"] == decoded_hash_code


def insert_client_sign():
    client_secret = "wCZ3dG4BUICAlS5DjEQr"
    # client_secret = "rLQ3DMjH6sbxr4ktFz2j"
    return client_secret


def make_dict_from_query(url: str)->dict:
    res = dict(
        parse_qsl(urlparse(url).query, keep_blank_values=True))
    return res


if __name__ == "__main__":

    url = "https://example.com/?vk_user_id=494075&vk_app_id=6736218&vk_is_app_user=1&vk_are_notifications_enabled=1&vk_language=ru&vk_access_token_settings=&vk_platform=android&sign=exTIBPYTrAKDTHLLm2AwJkmcVcvFCzQUNyoa6wAjvW6k"
    # Защищённый ключ из настроек вашего приложения
    client_secret = "ANZhZY0Ugu9rVA0esTjr"

    # Если без Flask или Django
    query_params = dict(parse_qsl(urlparse(url).query, keep_blank_values=True))
    status = is_valid(query=query_params, secret=client_secret)

    print("ok" if status else "fail")
