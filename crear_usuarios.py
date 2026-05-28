from app import create_app, db
from app.models import Usuario

app = create_app()

with app.app_context():
    jefe = Usuario(nombre='Jefe', email='jefe@inventario.com', rol='jefe')
    jefe.set_password('1234')
    db.session.add(jefe)

    trabajador = Usuario(nombre='Trabajador', email='trabajador@inventario.com', rol='trabajador')
    trabajador.set_password('1234')
    db.session.add(trabajador)

    db.session.commit()
    print('✅ Usuarios creados correctamente')