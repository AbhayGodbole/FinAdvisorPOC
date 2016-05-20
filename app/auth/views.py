from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, logout_user, login_required, session
from . import auth
from ..models import Advisor
from .forms import LoginForm
from .forms import RegisterForm
from ..import db


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db.create_all()
        advisor = Advisor.query.filter_by(email=form.email.data).first()
        if advisor is not None and advisor.verify_password(form.password.data):
            login_user(advisor, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.dashboard'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)

@auth.route('/Register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        db.create_all()
        advisor = Advisor(email=form.email.data, 
                          firstname=form.firstname.data, 
                          lastname=form.lastname.data,
                          password=form.password.data)
        db.session.add(advisor)
        flash('You can now login.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('auth.login'))
