from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# ------------------------------------
# MODELO: Usuario
# ------------------------------------
class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    
    id       = db.Column(db.Integer, primary_key=True)
    nombre   = db.Column(db.String(100), nullable=False)
    email    = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    
    # El rol define los permisos: 'jefe' o 'trabajador'
    rol      = db.Column(db.String(20), nullable=False, default='trabajador')
    
    def set_password(self, password_plano):
        """Convierte la contraseña en un hash seguro"""
        self.password = generate_password_hash(password_plano)
    
    def check_password(self, password_plano):
        """Verifica si la contraseña ingresada es correcta"""
        return check_password_hash(self.password, password_plano)
    
    def es_jefe(self):
        """Devuelve True si el usuario es jefe"""
        return self.rol == 'jefe'
    
    def __repr__(self):
        return f'<Usuario {self.nombre} - {self.rol}>'

# ------------------------------------
# MODELO: Producto
# ------------------------------------
class Producto(db.Model):
    __tablename__ = 'productos'

    id            = db.Column(db.Integer, primary_key=True)
    nombre        = db.Column(db.String(100), nullable=False)
    descripcion   = db.Column(db.String(255))
    cantidad      = db.Column(db.Integer, nullable=False, default=0)
    precio        = db.Column(db.Float, nullable=False, default=0.0)
    categoria     = db.Column(db.String(50))

    # Especificaciones del celular
    marca         = db.Column(db.String(50))
    almacenamiento= db.Column(db.String(50))
    ram           = db.Column(db.String(50))
    color         = db.Column(db.String(50))
    camara_trasera= db.Column(db.String(100))
    camara_frontal= db.Column(db.String(100))
    bateria       = db.Column(db.String(50))
    cargador_watts= db.Column(db.String(50))
    conectividad  = db.Column(db.String(50))
    imei1         = db.Column(db.String(20))
    imei2         = db.Column(db.String(20))

    # Tienda
    tienda        = db.Column(db.String(50), default='Shiloh Store')

    def __repr__(self):
        return f'<Producto {self.nombre}>'

# ------------------------------------
# Requerido por Flask-Login
# Le dice cómo cargar un usuario por su ID
# ------------------------------------
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# ------------------------------------
# MODELO: Venta
# ------------------------------------
from datetime import datetime

class Venta(db.Model):
    __tablename__ = 'ventas'

    id           = db.Column(db.Integer, primary_key=True)
    cantidad     = db.Column(db.Integer, nullable=False)
    monto_total  = db.Column(db.Float, nullable=False)
    fecha        = db.Column(db.DateTime, default=datetime.utcnow)

    # Relación con producto y usuario
    producto_id  = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    usuario_id   = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    producto     = db.relationship('Producto', backref='ventas')
    usuario      = db.relationship('Usuario', backref='ventas')

    def __repr__(self):
        return f'<Venta {self.producto_id} - {self.cantidad}>'