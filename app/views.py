from flask import Blueprint, render_template, redirect, url_for, flash
from loguru import logger
from .forms import ContactForm

logger.add("app/logs/contacts.log", rotation="500 KB", level="INFO")

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def home():
    return render_template("base.html", title="Головна")


@main_bp.route('/resume')
def resume():
    return render_template("resume.html", title="Резюме")


@main_bp.route('/contacts', methods=['GET', 'POST'])
def contacts():
    form = ContactForm()

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        phone = form.phone.data
        subject = form.subject.data
        message = form.message.data

        logger.info(
            f"Контактна форма відправлена: Ім'я: {name}, Email: {email}, Телефон: {phone}, Тема: {subject}, Повідомлення: {message}")

        flash(f"Дякуємо, {name}! Ваше повідомлення з email {email} було успішно відправлено.", 'success')

        return redirect(url_for('main.contacts'))

    return render_template('contacts.html', title='Контакти', form=form)
