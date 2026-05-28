import os

class Config:
    # Clave secreta para las sesiones (cámbiala en producción)
    SECRET_KEY = 'mi_clave_secreta_123'
    
    # Ruta de la base de datos SQLite
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'inventario.db')
    
    # Evita warnings innecesarios
    SQLALCHEMY_TRACK_MODIFICATIONS = False