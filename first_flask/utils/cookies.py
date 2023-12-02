import json
from flask import request, url_for, redirect, make_response


def make_cookies(user, path):
    users = json.loads(request.cookies.get('users', json.dumps([])))
    users.append(user)
    encoded_users = json.dumps(users)
    response = make_response(redirect(url_for(path), code=302))
    response.set_cookie('users', encoded_users)
    return response


def update_cookies(users, path):
    encoded_users = json.dumps(users)
    response = make_response(redirect(url_for(path), code=302))
    response.set_cookie('users', encoded_users)
    return response
