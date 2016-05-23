from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required, Email, Length, ValidationError, URL
from ..models import Client

class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')
    
class ClientRegisterForm(Form):
    firstname = StringField('First Name', validators=[Required()])
    lastname = StringField('Last Name', validators=[Required()])
    email = StringField('Contact Email', validators=[Required(), Length(1, 64),Email()])
    address = TextAreaField('address', validators=[Required()])
    mobilenumber =StringField('Mobile Number', validators=[Required()])
    submit = SubmitField('Register')
    
    def validate_email(self, field):
        if Client.query.filter_by(email=field.data).first():
            raise ValidationError('Client already registered with this Email ID.')

class IdentifyOpportunityTextForm(Form) :
    text = TextAreaField('Enter Text Here', validators=[Required()])
    textGo = SubmitField('Submit to AlchemyLanguage')
    
class IdentifyOpportunityURLForm(Form) :
    text = StringField('Enter URL Here', validators=[Required(),URL()])
    urlGo = SubmitField('Submit to AlchemyLanguage')

class IdentifyOpportunityHTMLForm(Form) :
    text = TextAreaField('Enter HTML Here', validators=[Required()])
    htmlGo = SubmitField('Submit to AlchemyLanguage')    