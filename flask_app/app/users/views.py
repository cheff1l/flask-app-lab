from flask import render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from . import users_bp
from .forms import RegistrationForm, LoginForm, UpdateAccountForm, ChangePasswordForm
from .models import User
from app import db
import secrets
import os
from PIL import Image
from datetime import datetime, timezone


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'users/static/profile_pics', picture_fn)

    os.makedirs(os.path.dirname(picture_path), exist_ok=True)

    output_size = (128, 128)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@users_bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()


@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('users.account'))

    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = User().hash_password(form.password.data)
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            image='profile_default.jpg'  # Додаємо дефолтне зображення
        )
        db.session.add(user)
        db.session.commit()

        flash(f'Account created for {form.username.data}!', 'success')
        login_user(user)
        return redirect(url_for('users.account'))

    return render_template('users/register.html', form=form, title='Register')


@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users.account'))

    form = LoginForm()

    if form.validate_on_submit():
        user = db.session.execute(
            db.select(User).where(User.email == form.email.data)
        ).scalar_one_or_none()

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash('You logged in successfully!', 'success')
            return redirect(url_for('users.account'))
        else:
            flash('Error: Invalid username or password.', 'danger')

    return render_template('users/login.html', form=form, title='Login')


@users_bp.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me

    image_file = url_for('users.static', filename='profile_pics/' + current_user.image)
    return render_template('users/account.html',
                           user=current_user,
                           form=form,
                           image_file=image_file,
                           title='Account')


@users_bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        if current_user.check_password(form.current_password.data):
            hashed_password = current_user.hash_password(form.new_password.data)
            current_user.password = hashed_password
            db.session.commit()
            flash('Your password has been changed successfully!', 'success')
            return redirect(url_for('users.account'))
        else:
            flash('Current password is incorrect.', 'danger')

    return render_template('users/change_password.html', form=form, title='Change Password')


@users_bp.route('/logout')
def logout():
    logout_user()
    flash('You have successfully logged out.', 'info')
    return redirect(url_for('users.login'))


@users_bp.route('/all')
@login_required
def all_users():
    users = db.session.execute(db.select(User)).scalars().all()
    return render_template('users/all_users.html', users=users)