import requests
from django.conf import settings

def authorize_token(phone_number, password):
    response = requests.post(
        settings.AUTH_SERVER_DOMAIN+'/o/token/',
        data={
            'grant_type': 'password',
            'username': phone_number,
            'password': password,
            'client_id': settings.CLIENT_ID,
            'client_secret': settings.CLIENT_SECRET,
        },
    )
    return response


def revoke_token(token):
    response = requests.post(
        settings.AUTH_SERVER_DOMAIN+'/o/revoke_token/',
        data={
            'token': token,
            'client_id': settings.CLIENT_ID,
            'client_secret': settings.CLIENT_SECRET,
        },
    )
    return response
