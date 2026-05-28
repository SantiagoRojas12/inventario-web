from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Producto, Usuario

main = Blueprint('main', __name__)

# ------------------------------------
# RUTA: Dashboard con buscador y stats
# ------------------------------------
@main.route('/')
@main.route('/dashboard')
@login_required
def dashboard():
    busqueda = request.args.get('buscar', '')

    if busqueda:
        productos = Producto.query.filter(
            Producto.nombre.ilike(f'%{busqueda}%') |
            Producto.categoria.ilike(f'%{busqueda}%')
        ).all()
    else:
        productos = Producto.query.all()

    # Estadísticas
    total_productos  = Producto.query.count()
    stock_bajo       = Producto.query.filter(Producto.cantidad < 5).count()
    valor_total      = db.session.query(db.func.sum(Producto.precio * Producto.cantidad)).scalar() or 0

    return render_template('dashboard.html',
        usuario         = current_user,
        productos       = productos,
        busqueda        = busqueda,
        total_productos = total_productos,
        stock_bajo      = stock_bajo,
        valor_total     = valor_total
    )

# ------------------------------------
# RUTA: Agregar producto
# ------------------------------------
@main.route('/agregar', methods=['GET', 'POST'])
@login_required
def agregar():
    if not current_user.es_jefe():
        flash('No tienes permisos para esta acción', 'danger')
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        nombre      = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        cantidad    = request.form.get('cantidad')
        precio      = request.form.get('precio')
        categoria   = request.form.get('categoria')

        producto = Producto(
            nombre=nombre,
            descripcion=descripcion,
            cantidad=int(cantidad),
            precio=float(precio),
            categoria=categoria
        )
        db.session.add(producto)
        db.session.commit()
        flash('Producto agregado correctamente', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('agregar.html', usuario=current_user)

# ------------------------------------
# RUTA: Editar producto
# ------------------------------------
@main.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    if not current_user.es_jefe():
        flash('No tienes permisos para esta acción', 'danger')
        return redirect(url_for('main.dashboard'))

    producto = Producto.query.get_or_404(id)

    if request.method == 'POST':
        producto.nombre      = request.form.get('nombre')
        producto.descripcion = request.form.get('descripcion')
        producto.cantidad    = int(request.form.get('cantidad'))
        producto.precio      = float(request.form.get('precio'))
        producto.categoria   = request.form.get('categoria')

        db.session.commit()
        flash('Producto actualizado correctamente', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('editar.html', usuario=current_user, producto=producto)

# ------------------------------------
# RUTA: Eliminar producto
# ------------------------------------
@main.route('/eliminar/<int:id>')
@login_required
def eliminar(id):
    if not current_user.es_jefe():
        flash('No tienes permisos para esta acción', 'danger')
        return redirect(url_for('main.dashboard'))

    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    flash('Producto eliminado correctamente', 'success')
    return redirect(url_for('main.dashboard'))

# ------------------------------------
# RUTA: Gestión de usuarios
# ------------------------------------
@main.route('/usuarios')
@login_required
def usuarios():
    if not current_user.es_jefe():
        flash('No tienes permisos para esta acción', 'danger')
        return redirect(url_for('main.dashboard'))

    usuarios = Usuario.query.all()
    return render_template('usuarios.html', usuario=current_user, usuarios=usuarios)

# ------------------------------------
# RUTA: Crear usuario
# ------------------------------------
@main.route('/usuarios/crear', methods=['GET', 'POST'])
@login_required
def crear_usuario():
    if not current_user.es_jefe():
        flash('No tienes permisos para esta acción', 'danger')
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        nombre   = request.form.get('nombre')
        email    = request.form.get('email')
        password = request.form.get('password')
        rol      = request.form.get('rol')

        if Usuario.query.filter_by(email=email).first():
            flash('Ya existe un usuario con ese email', 'danger')
            return redirect(url_for('main.crear_usuario'))

        nuevo = Usuario(nombre=nombre, email=email, rol=rol)
        nuevo.set_password(password)
        db.session.add(nuevo)
        db.session.commit()
        flash('Usuario creado correctamente', 'success')
        return redirect(url_for('main.usuarios'))

    return render_template('crear_usuario.html', usuario=current_user)

# ------------------------------------
# RUTA: Eliminar usuario
# ------------------------------------
@main.route('/usuarios/eliminar/<int:id>')
@login_required
def eliminar_usuario(id):
    if not current_user.es_jefe():
        flash('No tienes permisos para esta acción', 'danger')
        return redirect(url_for('main.dashboard'))

    if id == current_user.id:
        flash('No puedes eliminarte a ti mismo', 'danger')
        return redirect(url_for('main.usuarios'))

    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    flash('Usuario eliminado correctamente', 'success')
    return redirect(url_for('main.usuarios'))