from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, ValidationError


class ContactForm(FlaskForm):
    name = StringField('Ім\'я', validators=[
        DataRequired(message="Це поле обов'язкове"),
        Length(min=4, max=10, message="Ім'я повинно бути від 4 до 10 символів")
    ])

    email = StringField('Email', validators=[
        DataRequired(message="Це поле обов'язкове"),
        Email(message="Будь ласка, введіть коректну email адресу")
    ])

    phone = StringField('Телефон', validators=[
        DataRequired(message="Це поле обов'язкове"),
        Regexp(r'^\+380\d{9}$', message="Телефон має бути у форматі +380XXXXXXXXX")
    ])

    subject = SelectField('Тема', choices=[
        ('general', 'Загальні питання'),
        ('technical', 'Технічні питання'),
        ('cooperation', 'Співпраця'),
        ('feedback', 'Відгук')
    ], validators=[DataRequired(message="Це поле обов'язкове")])

    message = TextAreaField('Повідомлення', validators=[
        DataRequired(message="Це поле обов'язкове"),
        Length(max=500, message="Повідомлення не повинно перевищувати 500 символів")
    ])

    submit = SubmitField('Надіслати')


class LoginForm(FlaskForm):
    username = StringField('Ім\'я користувача', validators=[
        DataRequired(message="Це поле обов'язкове")
    ])

    password = PasswordField('Пароль', validators=[
        DataRequired(message="Це поле обов'язкове"),
        Length(min=4, max=10, message="Пароль повинен бути від 4 до 10 символів")
    ])

    remember = BooleanField('Запам\'ятати мене')

    submit = SubmitField('Увійти')