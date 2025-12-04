from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import users_bp
from .forms import RegistrationForm, LoginForm
from .models import User
from app import db


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
            password=hashed_password
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


@users_bp.route('/account')
@login_required
def account():
    return render_template('users/account.html', user=current_user)


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
