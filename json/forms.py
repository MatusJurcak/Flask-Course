from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, IntegerField, validators

class SignupForm(FlaskForm):
    name = StringField('Name', [validators.Length(min=1)])
    email = StringField('E-mail', [validators.Length(min=6, max=35)])
    favorite_number = IntegerField('Favorite Number')
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    newsletter = BooleanField('Sign me up for your newsletter!')
