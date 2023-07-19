from itsdangerous import URLSafeTimedSerializer as Serializer
from . import db
from flask import current_app
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(1000), nullable=False)
    username = db.Column(db.String(10), nullable=False)
    notes = db.relationship('Note', backref='author', lazy=True)
    
    def get_reset_token(self):
        s = Serializer(current_app.config['SECRET_KEY'], 'confirmation')
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token, max_age=1800):
        s = Serializer(current_app.config['SECRET_KEY'], 'confirmation')
        try:
            user_id = s.loads(token, max_age=max_age)['user_id']
        except:
            return None
        return User.query.get(user_id)
        
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"Note('{self.text}', '{self.date}', '{self.user_id}')"

