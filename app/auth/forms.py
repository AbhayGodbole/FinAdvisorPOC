from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, EqualTo, ValidationError
from ..models import Advisor


class LoginForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')
    
class RegisterForm(Form):
    firstname = StringField('First Name', validators=[Required()])
    lastname = StringField('Last Name', validators=[Required()])
    email = StringField('Email (UserID)', validators=[Required(), Length(1, 64),Email()])
    password = PasswordField('Password', validators=[Required(), EqualTo('confirmpassword', message='Passwords must match.')])
    confirmpassword = PasswordField('Conform Password', validators=[Required()])
    submit = SubmitField('Register')
    
    def validate_email(self, field):
        if Advisor.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')
    