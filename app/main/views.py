from flask import render_template, redirect, request, url_for, flash, jsonify
from flask.ext.login import login_user, logout_user, login_required, session, current_user
from . import main
from ..models import Client, Advisor
from .forms import ClientRegisterForm
from .. import db
from app.main.forms import IdentifyOpportunityTextForm, IdentifyOpportunityURLForm, IdentifyOpportunityHTMLForm
import json
from ..Watson import Services
from app.Watson.Services import getConcepts, getKeywords

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
    """   textForm = IdentifyOpportunityForm()
    
    if textForm.validate_on_submit() and textForm.textGo.data:
        response = Services.AlchemyLanguageText(textForm.text.data)
        return render_template('idntfyOpportunity.html', form=textForm,var="yes",response=response)
    """
    form = IdentifyOpportunityTextForm()
    return render_template('idntfyOpportunity.html', form=form)
 
@main.route('/processText',  methods=['GET', 'POST'])
def ProcessText():
    textForm = IdentifyOpportunityTextForm()
    if textForm.validate_on_submit() and textForm.textGo.data:
        response = Services.AlchemyLanguageText(textForm.text.data,"Text")
        
        """ Extract the Concepts and Keywords """
        concepts = getConcepts(response)
        print ("###### ",concepts)
        keywords = getKeywords(response)
        RecommendationsOnConcepts  = Services.AlchemyDataNewsConcept(concepts)
        RecommendationsOnKeywords = Services.AlchemyDataNewsKeyword(keywords)
    
        return render_template('textForm.html', form=textForm,var="yes",response=response, concepts=concepts, keywords=keywords, RecommendationsOnConcepts  = json.loads(RecommendationsOnConcepts), RecommendationsOnKeywords  = json.loads(RecommendationsOnKeywords ))
    return render_template('textForm.html', form=textForm)   
    
@main.route('/processURL',  methods=['GET', 'POST'])
def ProcessURL():
    urlForm = IdentifyOpportunityURLForm()
    if urlForm.validate_on_submit() and urlForm.urlGo.data:
        response = Services.AlchemyLanguageText(urlForm.text.data,"Url")
        
        """ Extract the Concepts and Keywords """
        concepts = getConcepts(response)
        keywords = getKeywords(response)
        
        RecommendationsOnConcepts  = Services.AlchemyDataNewsConcept(concepts)
        RecommendationsOnKeywords = Services.AlchemyDataNewsKeyword(keywords)
        
        return render_template('urlForm.html', form=urlForm,var="yes",response=response, concepts=concepts, keywords=keywords, RecommendationsOnConcepts  = json.loads(RecommendationsOnConcepts), RecommendationsOnKeywords  = json.loads(RecommendationsOnKeywords ))
    
    return render_template('urlForm.html', form=urlForm)

@main.route('/processHTML',  methods=['GET', 'POST'])
def ProcessHTML():
    htmlForm = IdentifyOpportunityHTMLForm()
    if htmlForm.validate_on_submit() and htmlForm.htmlGo.data:
        response = Services.AlchemyLanguageText(htmlForm.text.data,"HTML")
        
        """ Extract the Concepts and Keywords """
        concepts = getConcepts(response)
        keywords = getKeywords(response)
        
        return render_template('htmlForm.html', form=htmlForm,var="yes",response=response, concepts=concepts, keywords=keywords)
    
    return render_template('htmlForm.html', form=htmlForm)      
    