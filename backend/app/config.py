import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:3.1415926@127.0.0.1:45608/crm_flask'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Celery - Using SQLAlchemy (Database) as broker and backend
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL') or 'sqla+mysql+pymysql://root:3.1415926@127.0.0.1:45608/crm_flask'
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND') or 'db+mysql+pymysql://root:3.1415926@127.0.0.1:45608/crm_flask'
    
    # JWT
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key'
