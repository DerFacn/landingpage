from datetime import datetime, timedelta
from flask import Flask, current_app, request, redirect, make_response, render_template
from app.utils import get_tokens_with_code, refresh_access_token, get_userinfo, auth_required


def register_functions(app: Flask):
    app.add_url_rule('/', 'index', index, methods=['GET'])
    app.add_url_rule('/auth', 'auth', auth, methods=['GET'])
    app.add_url_rule('/admin', 'admin', admin, methods=['GET'])
    app.add_url_rule('/logout', 'logout', logout, methods=['GET'])


def index():
    access_token = request.cookies.get('access_token')

    if not access_token:
        client_id = current_app.config.get('CLIENT_ID')
        auth_url = current_app.config.get('AUTH_URL')
        redirect_uri = current_app.config.get('REDIRECT_URI')
        url = auth_url + f"?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope=openid%20profile"
        return redirect(url)

    refreshed = False
    try:
        user_info = get_userinfo()
    except:
        try:
            # If access token expired
            access_token = refresh_access_token()

            user_info = get_userinfo(access_token)
            refreshed = True
        except:
            # If refresh token expired too then reset all the tokens and go to the auth
            resp = make_response(redirect('/'))
            resp.set_cookie('refresh_token', '')
            resp.set_cookie('access_token', '')
            return resp

    if refreshed:
        resp = make_response(render_template('index.html', user_info=user_info))
        resp.set_cookie('access_token', access_token)
        return resp

    return render_template('index.html', user_info=user_info)


def auth():
    code = request.args.get('code')

    try:
        data = get_tokens_with_code(code)
    except:
        return {"message": "Try again later"}
    
    expiration = datetime.now() + timedelta(days=400)
    response = make_response(redirect('/'))
    response.set_cookie('access_token', data.get('access_token'), expires=expiration)
    response.set_cookie('refresh_token', data.get('refresh_token'), expires=expiration)

    return response


@auth_required
def admin(user_info: dict, access_token: str | None):
    if access_token:
        resp = make_response(render_template('admin.html', user_info=user_info))
        resp.set_cookie('access_token', access_token)
        return resp
    
    return render_template('admin.html', user_info=user_info)


def logout():
    logout_url = current_app.config.get('LOGOUT_URL')
    response = make_response(redirect(logout_url))
    response.set_cookie('access_token', '')
    response.set_cookie('refresh_token', '')

    return response
