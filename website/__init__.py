from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_mail import Mail
from website.config import Config 

db = SQLAlchemy()
DB_NAME='database.db'
    
from website.models import User
        
login_manager = LoginManager()
login_manager.login_view = 'users.login'

mail = Mail()

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    
    from website.users.routes import users
    from website.notes.routes import notes
    from website.main.routes import main
    from website.errors.routes import errors

    app.register_blueprint(users, url_prefix='/')
    app.register_blueprint(notes, url_prefix='/')
    app.register_blueprint(main, url_prefix='/')
    app.register_blueprint(errors, url_prefix='/')

    
    login_manager.init_app(app)
    
    db.init_app(app)
    
    mail.init_app(app)
    
    with app.app_context():
        if not path.exists('website/' + DB_NAME):
            db.create_all()
            print('Created Database!')
    
    return app
