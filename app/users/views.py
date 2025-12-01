from flask import render_template, request, redirect, url_for, flash, session, make_response
from . import users_bp
from ..forms import LoginForm
from functools import wraps
from datetime import datetime, timedelta

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Спочатку потрібно увійти в систему!', 'danger')
            return redirect(url_for('users.login'))
        return f(*args, **kwargs)

    return decorated_function


@users_bp.route('/hi/<string:name>')
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, int)
    return render_template("users/hi.html", name=name, age=age)


@users_bp.route('/admin')
def admin():
    to_url = url_for("users.greetings", name="administrator", age=45, _external=True)
    print(to_url)
    return redirect(to_url)

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data

        if username == 'admin' and password == 'password':
            session['username'] = username

            remember_msg = "з опцією 'Запам'ятати мене'" if remember else "без опції 'Запам'ятати мене'"
            flash(f'Ви успішно увійшли в систему {remember_msg}!', 'success')

            return redirect(url_for('users.profile'))
        else:
            flash('Неправильне ім\'я користувача або пароль!', 'danger')

    return render_template('users/login.html', title='Вхід', form=form)


@users_bp.route('/profile')
@login_required
def profile():
    return render_template('users/profile.html', title='Профіль')


@users_bp.route('/logout')
def logout():
    session.pop('username', None)
    flash('Ви успішно вийшли з системи!', 'success')
    return redirect(url_for('users.login'))


@users_bp.route('/set-color/<scheme>')
@login_required
def set_color(scheme):
    if scheme in ['light', 'dark']:
        session['color_scheme'] = scheme
        flash(f'Кольорова схема змінена на {scheme}!', 'success')
    return redirect(url_for('users.profile'))


@users_bp.route('/add-cookie', methods=['POST'])
@login_required
def add_cookie():
    key = request.form.get('key')
    value = request.form.get('value')
    days = request.form.get('days', type=int)

    if not key or not value:
        flash('Ключ та значення кукі обов\'язкові!', 'danger')
        return redirect(url_for('users.profile'))

    response = make_response(redirect(url_for('users.profile')))
    expires = None
    if days:
        expires = datetime.now() + timedelta(days=days)

    response.set_cookie(key, value, expires=expires)
    flash(f'Кукі {key} успішно додано!', 'success')
    return response


@users_bp.route('/delete-cookie', methods=['POST'])
@login_required
def delete_cookie():
    key = request.form.get('key')

    if not key:
        flash('Ключ кукі обов\'язковий!', 'danger')
        return redirect(url_for('users.profile'))

    response = make_response(redirect(url_for('users.profile')))
    response.delete_cookie(key)
    flash(f'Кукі {key} успішно видалено!', 'success')
    return response


@users_bp.route('/delete-all-cookies', methods=['POST'])
@login_required
def delete_all_cookies():
    response = make_response(redirect(url_for('users.profile')))

    for key in request.cookies.keys():
        if key != 'session':
            response.delete_cookie(key)

    flash('Всі кукі успішно видалено!', 'success')
    return response