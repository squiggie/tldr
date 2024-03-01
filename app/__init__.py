from flask import Flask
from config import Config, DevelopmentConfig, ProductionConfig
from extensions import db, migrate
import os
from app import routes
from flask_login import LoginManager
from app.models import User

def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)
    app.config.from_pyfile('config.py', silent=True)

    print("Loading Login Manager")
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        print('Loading user:', user_id)
        user = User.query.get(int(user_id))
        print('Loaded user:', user)
        return user

    routes.init_app(app)

    if os.getenv('FLASK_ENV') == 'production':
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)
    
    db.init_app(app)
    with app.app_context():
        db.create_all()
    migrate.init_app(app, db)
        
    return app
