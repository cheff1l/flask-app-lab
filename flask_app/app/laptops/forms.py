from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class LaptopForm(FlaskForm):
    brand = StringField('Brand', validators=[
        DataRequired(),
        Length(min=2, max=100)
    ])

    model = StringField('Model', validators=[
        DataRequired(),
        Length(min=2, max=100)
    ])

    price = FloatField('Price (USD)', validators=[
        DataRequired(),
        NumberRange(min=0, message="Price must be positive")
    ])

    description = TextAreaField('Description', validators=[
        Length(max=500)
    ])

    category_id = SelectField('Category', coerce=int, validators=[
        DataRequired()
    ])

    submit = SubmitField('Save')


class SearchForm(FlaskForm):
    search_query = StringField('Search by brand or model', validators=[
        Length(max=100)
    ])

    submit = SubmitField('Search')