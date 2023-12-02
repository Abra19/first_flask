import json
import os
import time
from dotenv import load_dotenv
from flask import (
    Flask,
    render_template,
    request,
    url_for,
    redirect,
    flash,
    get_flashed_messages,
    session
)
from first_flask.utils.validate import validate
from first_flask.utils.cookies import make_cookies, update_cookies
from first_flask.utils.get_user import get_user
from first_flask.utils.find_obj import find_obj_by_id
from first_flask.users.users import users

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def main():
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'index.html',
        messages=messages
    )


@app.route('/users_start')
def start_users():
    return render_template(
        'users/users.html'
    )


@app.get('/users')
def get_users():
    search_datas = request.args.get('search_form', '')
    users = json.loads(request.cookies.get('users', json.dumps([])))
    filtered_users = list(
        filter(
            lambda item: search_datas.lower() in item['nickname'].lower(),
            users
        )
    ) if search_datas else users
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        '/users/index.html',
        users=filtered_users,
        search=search_datas,
        messages=messages
    )


@app.post('/users')
def post_new_user():
    user = request.form.to_dict()
    errors = validate(user)
    if errors:
        return render_template(
            '/users/new.html',
            user=user,
            errors=errors
        )
    id = int(time.time())
    user['id'] = id
    return make_cookies(user, 'get_users')


@app.route('/users/new')
def new_user():
    user = {
        'nickname': '',
        'email': ''
    }
    errors = {}
    return render_template(
        '/users/new.html',
        user=user,
        errors=errors
    )


@app.route('/users/<id>/edit')
def edit_user(id):
    users = json.loads(request.cookies.get('users', json.dumps([])))
    user = find_obj_by_id(users, int(id))
    errors = {}
    return render_template(
        '/users/edit.html',
        user=user,
        errors=errors
    )


@app.post('/user/<id>/patch')
def update_user(id):
    data = request.form.to_dict()
    errors = validate(data)
    users = json.loads(request.cookies.get('users', json.dumps([])))
    user = find_obj_by_id(users, int(id))
    for key in data:
        user[key] = data[key]
    if errors:
        return render_template(
            '/users/edit.html',
            user=user,
            errors=errors
        ), 422

    flash('User has been updated')
    return update_cookies(users, 'get_users')


@app.route('/users/<id>/delete', methods=['GET', 'POST'])
def delete_user(id):
    users = json.loads(request.cookies.get('users', json.dumps([])))
    user = find_obj_by_id(users, int(id))
    if request.method == 'GET':
        return render_template(
            '/users/delete.html',
            user=user
        )
    else:
        users.remove(user)
        flash('User has been deleted!', 'success')
        return update_cookies(users, 'get_users')


@app.route('/cart', methods=['GET'])
def index():
    cart = json.loads(request.cookies.get('cart', json.dumps({})))
    return render_template('carts/index.html', cart=cart)


@app.post('/cart-items')
def add_item():
    props = request.form.to_dict()
    cart = json.loads(request.cookies.get('cart', json.dumps({})))
    current = cart.get(props['item_id'])
    if current:
        current['count'] += 1
        cart[props['item_id']] = current
    else:
        cart.setdefault(
            props['item_id'],
            {'name': props['item_name'], 'count': 1}
        )

    encoded_cart = json.dumps(cart)
    response = redirect('/cart')
    response.set_cookie('cart', encoded_cart)
    return response


@app.post('/cart-items/clean')
def clean_cart():
    response = redirect('/cart')
    response.delete_cookie('cart')
    return response


@app.post('/session/new')
def create_session():
    data = request.form.to_dict()
    user = get_user(data, users)
    if not user:
        flash('Wrong password or name', 'error')
        return redirect('/')
    session['username'] = user
    return redirect(url_for('start_users'), 302)


@app.route('/session/delete', methods=['POST', 'DELETE'])
def delete_session():
    session.clear()
    return redirect(url_for('main'), 302)
