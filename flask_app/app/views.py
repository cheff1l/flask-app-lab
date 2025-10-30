import os
import logging
from loguru import logger
from flask import render_template, request, redirect, url_for, flash, session
from . import app
from .forms import ContactForm

logger.add("app/logs/contacts.log", rotation="500 KB", level="INFO")


@app.route('/')
def main():
    return render_template("base.html", title="Головна")


@app.route('/resume')
def resume():
    return render_template("resume.html", title="Резюме")


@app.route('/contacts', methods=['GET', 'POST'])
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

        return redirect(url_for('contacts'))

    return render_template('contacts.html', title='Контакти', form=form)