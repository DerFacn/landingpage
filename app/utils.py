import base64
import requests
from flask import current_app, request


def get_tokens_with_code(code: str):
    token_url = current_app.config.get('TOKEN_URL')
    client_id = current_app.config.get('CLIENT_ID')
    client_secret = current_app.config.get('CLIENT_SECRET')
    redirect_uri = current_app.config.get('REDIRECT_URI')

    if None in [token_url, client_secret, client_id]:
        raise Exception('Token url, client id or client secret is not provided!')

    response = requests.post(token_url, 
                             data={
                                 "code": code,
                                 "client_id": client_id,
                                 "client_secret": client_secret,
                                 "redirect_uri": redirect_uri,
                                 "grant_type": "authorization_code"
                             })

    data = response.json()
    access_token = data.get('access_token')
    refresh_token = data.get('refresh_token')

    if not access_token or not refresh_token:
        raise Exception(f'{response.content}')

    return {"access_token": access_token, "refresh_token": refresh_token}


def refresh_access_token():
    refresh_token = request.cookies.get('refresh_token')

    token_url = current_app.config.get('TOKEN_URL')
    client_id = current_app.config.get('CLIENT_ID')
    client_secret = current_app.config.get('CLIENT_SECRET')
    authorization = base64.b64encode(
        f'{client_id}:{client_secret}'.encode('utf-8')
    ).decode('utf-8')

    response = requests.post(token_url,
                             headers={
                                 "Authorization": f"Basic {authorization}"
                             },
                             data={
                                 "grant_type": "refresh_token",
                                 "client_id": client_id,
                                 "refresh_token": refresh_token
                             })
    
    data = response.json()

    return data.get('access_token')


def get_userinfo(token:str=None):
    userinfo_url = current_app.config.get('USERINFO_URL')
    access_token = request.cookies.get('access_token')

    response = requests.get(userinfo_url, 
                            headers={
                                "Authorization": f"Bearer {token if token else access_token}"
                            })
    
    if response.status_code == 401:
        raise Exception('Unauthorized!')
    
    return response.json()
