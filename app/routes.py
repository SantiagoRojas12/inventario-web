from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Producto, Usuario, Venta

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
        producto = Producto(
            nombre         = request.form.get('nombre'),
            descripcion    = request.form.get('descripcion'),
            cantidad       = int(request.form.get('cantidad')),
            precio         = float(request.form.get('precio')),
            categoria      = request.form.get('categoria'),
            marca          = request.form.get('marca'),
            almacenamiento = request.form.get('almacenamiento'),
            color          = request.form.get('color'),
            camara_trasera = request.form.get('camara_trasera'),
            camara_frontal = request.form.get('camara_frontal'),
            bateria        = request.form.get('bateria'),
            cargador_watts = request.form.get('cargador_watts'),
            conectividad   = request.form.get('conectividad'),
            imei1          = request.form.get('imei1'),
            imei2          = request.form.get('imei2'),
            tienda         = request.form.get('tienda')
        )
        db.session.add(producto)
        db.session.commit()
        flash('Producto agregado correctamente', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('agregar.html', usuario=current_user)

# ------------------------------------
# RUTA: Ver detalle producto
# ------------------------------------
@main.route('/producto/<int:id>')
@login_required
def detalle_producto(id):
    producto = Producto.query.get_or_404(id)
    return render_template('detalle_producto.html', producto=producto)

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
        producto.nombre         = request.form.get('nombre')
        producto.descripcion    = request.form.get('descripcion')
        producto.cantidad       = int(request.form.get('cantidad'))
        producto.precio         = float(request.form.get('precio'))
        producto.categoria      = request.form.get('categoria')
        producto.marca          = request.form.get('marca')
        producto.almacenamiento = request.form.get('almacenamiento')
        producto.color          = request.form.get('color')
        producto.camara_trasera = request.form.get('camara_trasera')
        producto.camara_frontal = request.form.get('camara_frontal')
        producto.bateria        = request.form.get('bateria')
        producto.cargador_watts = request.form.get('cargador_watts')
        producto.conectividad   = request.form.get('conectividad')
        producto.imei1          = request.form.get('imei1')
        producto.imei2          = request.form.get('imei2')
        producto.tienda         = request.form.get('tienda')

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
    
    # Elimina primero las ventas relacionadas
    Venta.query.filter_by(producto_id=id).delete()
    
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
# RUTA: Editar usuario
# ------------------------------------
@main.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_usuario(id):
    if not current_user.es_jefe():
        flash('No tienes permisos para esta acción', 'danger')
        return redirect(url_for('main.dashboard'))

    usuario = Usuario.query.get_or_404(id)

    if request.method == 'POST':
        nombre   = request.form.get('nombre')
        email    = request.form.get('email')
        rol      = request.form.get('rol')
        password = request.form.get('password')

        existe = Usuario.query.filter_by(email=email).first()
        if existe and existe.id != id:
            flash('Ese email ya está en uso', 'danger')
            return redirect(url_for('main.editar_usuario', id=id))

        usuario.nombre = nombre
        usuario.email  = email
        usuario.rol    = rol

        if password:
            usuario.set_password(password)

        db.session.commit()
        flash('Usuario actualizado correctamente', 'success')
        return redirect(url_for('main.usuarios'))

    return render_template('editar_usuario.html', usuario_edit=usuario)

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

# ------------------------------------
# RUTA: Formulario de venta
# ------------------------------------
@main.route('/vender/form/<int:id>')
@login_required
def vender_form(id):
    producto = Producto.query.get_or_404(id)
    return render_template('vender.html', producto=producto)

# ------------------------------------
# RUTA: Registrar venta
# ------------------------------------
@main.route('/vender/<int:id>', methods=['POST'])
@login_required
def vender(id):
    producto = Producto.query.get_or_404(id)
    cantidad = int(request.form.get('cantidad'))

    if cantidad <= 0:
        flash('La cantidad debe ser mayor a 0', 'danger')
        return redirect(url_for('main.dashboard'))

    if cantidad > producto.cantidad:
        flash(f'Stock insuficiente. Solo hay {producto.cantidad} unidades', 'danger')
        return redirect(url_for('main.dashboard'))

    producto.cantidad -= cantidad

    venta = Venta(
        cantidad    = cantidad,
        monto_total = cantidad * producto.precio,
        producto_id = producto.id,
        usuario_id  = current_user.id
    )
    db.session.add(venta)
    db.session.commit()

    flash(f'✅ Venta registrada: {cantidad} x {producto.nombre}', 'success')
    return redirect(url_for('main.dashboard'))

# ------------------------------------
# RUTA: Historial de ventas
# ------------------------------------
@main.route('/ventas')
@login_required
def ventas():
    if not current_user.es_jefe():
        flash('No tienes permisos para esta acción', 'danger')
        return redirect(url_for('main.dashboard'))

    ventas = Venta.query.order_by(Venta.fecha.desc()).all()
    total_vendido = db.session.query(
        db.func.sum(Venta.monto_total)
    ).scalar() or 0

    return render_template('ventas.html',
        ventas        = ventas,
        total_vendido = total_vendido
    )