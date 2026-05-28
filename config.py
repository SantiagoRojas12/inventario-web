import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'mi_clave_secreta_123'
    
    # Usa PostgreSQL en Render o SQLite local
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///inventario.db'
    
    # Render usa 'postgres://' pero SQLAlchemy necesita 'postgresql://'
    if DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False