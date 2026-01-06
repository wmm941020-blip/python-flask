from flask import Flask
from .config import Config
from .extensions import db, migrate, jwt, celery
from flask_cors import CORS

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)
    
    # Configure Celery
    celery.conf.update(app.config)
    celery.conf.broker_url = app.config.get('CELERY_BROKER_URL')
    celery.conf.result_backend = app.config.get('CELERY_RESULT_BACKEND')
    # Ensure tasks are discovered
    celery.autodiscover_tasks(['app.tasks.export'])

    # Register Blueprints
    from .api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app
