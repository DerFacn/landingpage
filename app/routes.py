from flask import Flask, current_app, request, redirect, make_response
from app.utils import get_access_token_with_code, refresh_access_token, get_userinfo


def register_functions(app: Flask):
    app.add_url_rule('/', 'index', index, methods=['GET'])
    app.add_url_rule('/auth', 'auth', auth, methods=['GET'])
    app.add_url_rule('/logout', 'logout', logout, methods=['GET'])


def index():
    access_token = request.cookies.get('access_token')

    if not access_token:
        client_id = current_app.config.get('CLIENT_ID')
        auth_url = current_app.config.get('AUTH_URL')
        url = auth_url + f"?client_id={client_id}&response_type=code&redirect_uri=http://127.0.0.1:5000/auth&scope=openid%20profile"
        return redirect(url)
    
    try:
        user_info = get_userinfo()
    except:
        access_token = refresh_access_token()

    try:
        user_info = get_userinfo()
    except:
        response = make_response(redirect('/'))
        response.set_cookie('refresh_token', '')
        response.set_cookie('access_token', '')
        return response

    return {"message": user_info}


def auth():
    code = request.args.get('code')

    try:
        data = get_access_token_with_code(code)
    except:
        return {"message": "Try again later"}
    
    response = make_response(redirect('/'))
    response.set_cookie('access_token', data.get('access_token'))
    response.set_cookie('refresh_token', data.get('refresh_token'))

    return response


def logout():
    logout_url = current_app.config.get('LOGOUT_URL')
    response = make_response(redirect(logout_url))
    response.set_cookie('access_token', '')
    response.set_cookie('refresh_token', '')

    return response
