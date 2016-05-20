from flask import render_template, redirect, request, url_for, flash, jsonify
from flask.ext.login import login_user, logout_user, login_required, session, current_user
from . import main
from ..models import Client, Advisor
from .forms import ClientRegisterForm
from .. import db
from app.main.forms import IdentifyOpportunityForm, IdentifyOpportunityURLForm

from ..Watson import Services

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/contact')
def contact():
    return render_template('contact.html')

@main.route('/dashboard')
def dashboard():
    clients = Client.query.join(Advisor, Client.advisor_id==Advisor.id).filter(Client.advisor_id == current_user.id).all()
    return render_template('dashboard.html', clients=clients)

@main.route('/addClient', methods=['GET', 'POST'])
def addClient():
    form = ClientRegisterForm()
    if form.validate_on_submit():
        db.create_all()
        client = Client(
                        firstname=form.firstname.data,
                        lastname=form.lastname.data,
                        email=form.email.data,
                        address=form.address.data,
                        mobilenumber=form.mobilenumber.data,
                        advisor_id = current_user.id)
        db.session.add(client)
        flash('Client Registered Successfully.')
        return redirect(url_for('main.dashboard'))
    return render_template('addClient.html', form=form)


@main.route('/identifyOpportunity',  methods=['GET', 'POST'])
def identifyOpportunity():
    textForm = IdentifyOpportunityForm()
    
    if textForm.validate_on_submit() and textForm.textGo.data:
        response = Services.AlchemyLanguageText(textForm.text.data)
        return render_template('idntfyOpportunity.html', form=textForm,var="yes",response=response)
    
    return render_template('idntfyOpportunity.html', form=textForm)
 
@main.route('/idntfyOpportunity#url',  methods=['GET', 'POST'])
def identifyOpportunityUrl():
    print("in URL")
    urlForm = IdentifyOpportunityURLForm()
    if urlForm.validate_on_submit() and urlForm.urlGo.data:
        response = Services.AlchemyLanguageText(urlForm.text.data)
        return render_template('idntfyOpportunity.html', form=urlForm,var="yes",response=response)
    
    return render_template('idntfyOpportunity.html', form=urlForm)   
    
@main.route('/processURL#url',  methods=['GET', 'POST'])
def ProcessURL():
    print("IN..............")    

    