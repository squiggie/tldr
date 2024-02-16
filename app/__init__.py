from flask import Flask
from config import Config, DevelopmentConfig, ProductionConfig
from extensions import db, migrate
import os

def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)
    app.config.from_pyfile('config.py', silent=True)

    from app import models, routes
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
