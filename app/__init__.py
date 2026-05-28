from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Creamos las instancias globales
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # Carga la configuración
    app.config.from_object('config.Config')
    
    # Conecta los plugins a la app
    db.init_app(app)
    login_manager.init_app(app)
    
    # Si alguien no está logueado y entra a una página protegida,
    # lo manda al login
    login_manager.login_view = 'auth.login'
    
    # Registra los blueprints (rutas)
    from app.auth import auth as auth_blueprint
    from app.routes import main as main_blueprint
    
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    
    # Crea las tablas si no existen
    with app.app_context():
        db.create_all()
    
    return app