from flask import render_template, redirect, request, url_for, flash, jsonify
from flask.ext.login import login_user, logout_user, login_required, session, current_user
from . import main
from ..models import Client, Advisor
from .forms import ClientRegisterForm
from .. import db
from app.main.forms import IdentifyOpportunityForm

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

@main.route('/idntfyOpportunity',  methods=['GET', 'POST'])
def identifyOpportunity():
    form = IdentifyOpportunityForm()
    if form.validate_on_submit():
        response = Services.AlchemyLanguageText(form.text.data)
        return render_template('idntfyOpportunity.html', form=form,var="yes",response=response) #redirect(url_for('main.identifyOpportunity'),var="yes")
    
    return render_template('idntfyOpportunity.html', form=form)


    