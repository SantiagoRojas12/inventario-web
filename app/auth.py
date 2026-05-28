from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from app.models import Usuario

auth = Blueprint('auth', __name__)

# ------------------------------------
# RUTA: Login
# ------------------------------------
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form.get('email')
        password = request.form.get('password')

        # Busca el usuario en la base de datos
        usuario = Usuario.query.filter_by(email=email).first()

        # Verifica si existe y si la contraseña es correcta
        if not usuario or not usuario.check_password(password):
            flash('Email o contraseña incorrectos', 'danger')
            return redirect(url_for('auth.login'))

        # Inicia la sesión
        login_user(usuario)
        return redirect(url_for('main.dashboard'))

    # Si es GET simplemente muestra el formulario
    return render_template('login.html')


# ------------------------------------
# RUTA: Logout
# ------------------------------------
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))