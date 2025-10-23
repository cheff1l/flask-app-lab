from flask import request, redirect, url_for, render_template, abort
from . import app

@app.route('/')
def main():
    return render_template("base.html")

@app.route('/resume')
def resume():
    return render_template("resume.html", title="Резюме")

@app.route('/contacts')
def contacts():
    return render_template("contacts.html", title="Контакти")