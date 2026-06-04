import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev_key_local'
    
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///inventario.db'
    
    if DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False