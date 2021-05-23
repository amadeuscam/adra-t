import requests
import json
from django.conf import settings


def get_caducidades(endpoints: list) -> dict:
    token = settings.TOKEN_KEY_USER
    headers = {'Authorization': f'Token {token}', 'Content-Type': 'application/json'}

    data_ret = {}

    for endpoint in endpoints:
        url = f'{settings.SITE_DOAMIN}api/{endpoint}/'
        data_res = requests.get(url, headers=headers)
        data_ret[endpoint] = json.loads(data_res.content.decode('utf-8'))

    return data_ret

