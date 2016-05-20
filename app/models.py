from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin, current_user
from . import db, login_manager
import hashlib
from flask import request
from flask.ext.login import AnonymousUserMixin

class Anonymous(AnonymousUserMixin):
  def __init__(self):
    self.username = 'Guest'
    self.id = 0

class Advisor(UserMixin, db.Model):
    __tablename__ = 'advisors'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(64), index=True)
    lastname = db.Column(db.String(64), index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    avatar_hash = db.Column(db.String(32))
    clients = db.relationship('Client', lazy='dynamic', backref='Advisor')
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Advisor %r>' % self.firstname
    
    def gravatar(self, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = self.avatar_hash or \
               hashlib.md5(self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)
        
class Client (UserMixin, db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(64), index=True)
    lastname = db.Column(db.String(64),  index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    address = db.Column(db.String(256), index=True) 
    mobilenumber = db.Column(db.Integer, index=True)
    advisor_id = db.Column(db.Integer, db.ForeignKey('advisors.id'))

    def __repr__(self):
        return self.firstname + ":" + self.lastname  
        """client = []
        client.append(self.firstname)
        client.append(self.lastname)
        
        return str(client)"""
    
@login_manager.user_loader
def load_user(user_id):
    db.create_all()
    login_manager.anonymous_user = Anonymous
    return Advisor.query.get(int(user_id))