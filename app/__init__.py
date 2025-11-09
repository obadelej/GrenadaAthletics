from flask import Flask
from extensions import db, migrate
from app.config.settings import Config

def create_app(config_class=Config):
    """Application factory pattern"""
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints
    from app.blueprints.athletes import athletes_bp
    from app.blueprints.events import events_bp
    from app.blueprints.competitions import competitions_bp
    from app.blueprints.main import main_bp
    from app.blueprints.news import news_bp
    from app.blueprints.directors import directors_bp
    from app.blueprints.affiliates import affiliates_bp
    from app.blueprints.calendar import calendar_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(news_bp, url_prefix='/news')
    app.register_blueprint(athletes_bp, url_prefix='/athletes')
    app.register_blueprint(events_bp, url_prefix='/events')
    app.register_blueprint(competitions_bp, url_prefix='/competitions')
    app.register_blueprint(directors_bp, url_prefix='/directors')
    app.register_blueprint(affiliates_bp, url_prefix='/affiliates')
    app.register_blueprint(calendar_bp, url_prefix='/calendar')
    
    return app
