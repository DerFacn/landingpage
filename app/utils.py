import uuid
import requests
from flask import current_app, request


def generate_id() -> str:
    return str(uuid.uuid4())


def get_access_token_with_code(code: str):
    token_url = current_app.config.get('TOKEN_URL')
    client_id = current_app.config.get('CLIENT_ID')
    client_secret = current_app.config.get('CLIENT_SECRET')

    if None in [token_url, client_secret, client_id]:
        raise Exception('Token url, client id or client secret is not provided!')

    state = generate_id()  # CSRF Protection
    nonce = generate_id()  # Another protect method

    response = requests.post(token_url, 
                             data={
                                 "code": code,
                                 "client_id": client_id,
                                 "client_secret": client_secret,
                                 "redirect_uri": "http://127.0.0.1:5000/auth",
                                 "grant_type": "authorization_code",
                                 "state": state,
                                 "nonce": nonce
                             })
    
    data = response.json()
    access_token = data.get('access_token')
    refresh_token = data.get('refresh_token')

    return {"access_token": access_token, "refresh_token": refresh_token}


def refresh_access_token():
    refresh_token = request.cookies.get('refresh_token')

    token_url = current_app.config.get('TOKEN_URL')

    response = requests.post(token_url,
                             data={
                                 "grant_type": "refresh_token",
                                 "client_id": "edv",
                                 "refresh_token": refresh_token
                             })
    
    data = response.json()

    return data.get('access_token')


def get_userinfo():
    userinfo_url = current_app.config.get('USERINFO_URL')
    access_token = request.cookies.get('access_token')

    response = requests.get(userinfo_url, 
                            headers={
                                "Authorization": f"Bearer {access_token}"
                            })
    
    return response.json()
