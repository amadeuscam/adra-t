from django.core.management.base import BaseCommand, CommandError
from datetime import date
from adra.models import Persona, Alimentos
import json
import requests


class Command(BaseCommand):

    def handle(self, *args, **options):
        # myToken = '<token>'
        # myUrl = '<website>'
        # head = {'Authorization': 'token {}'.format(myToken)}
        # url = "https://gorest.co.in/public-api/users"
        # response = requests.get(url=url, headers={'Content-Type': 'application/json'})
        # data = json.loads(response.content.decode('utf-8'))
        url = 'http://164.90.211.207/api/personas/223/'
        headers = {'Authorization': 'Token 38afed8fc17b2a9297d9a8ea7922d574989d823e',
                   'Content-Type': 'application/json'}
        r = requests.get(url, headers=headers)
        data = json.loads(r.content.decode('utf-8'))
        print(data)
