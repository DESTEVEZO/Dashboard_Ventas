from flask import Blueprint, render_template, redirect, url_for, session, flash
from app.models import Categoria, Producto, Venta, Usuario
from app.forms import CategoriaForm, ProductoForm, VentaForm, LoginForm         
from app import db
from .forms import LoginForm
from flask_login import login_user, logout_user
from flask_login import login_user, login_required, logout_user, current_user
from app.fraude.modelos_fraude import predecir_fraude
from flask import render_template, request, flash


main_bp = Blueprint('main_bp', __name__)

# ------------------------
# Dashboard principal
# ------------------------
@main_bp.route('/')
def dashboard():
    return render_template('dashboard.html')

# ------------------------
# Categorías
# ------------------------
@main_bp.route('/categorias')
def listar_categorias():
    categorias = Categoria.query.all()
    return render_template('categorias/listar.html', categorias=categorias)

@main_bp.route('/categorias/nueva', methods=['GET', 'POST'])
def nueva_categoria():
    form = CategoriaForm()
    if form.validate_on_submit():
        categoria = Categoria(
            nombre=form.nombre.data,
            descripcion=form.descripcion.data,
            estado=form.estado.data
        )
        db.session.add(categoria)
        db.session.commit()
        flash('Categoría agregada exitosamente.')
        return redirect(url_for('main_bp.listar_categorias'))
    return render_template('categorias/nueva.html', form=form)


# -----------------------
# Editar categorias
# -----------------------

@main_bp.route('/categorias/editar/<int:id>', methods=['GET', 'POST'])
def editar_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    form = CategoriaForm(obj=categoria)

    if form.validate_on_submit():
        categoria.nombre = form.nombre.data
        categoria.descripcion = form.descripcion.data
        categoria.estado = form.estado.data

        db.session.commit()
        flash('Categoría actualizada correctamente.')
        return redirect(url_for('main_bp.listar_categorias'))

    return render_template('categorias/nueva.html', form=form, categoria=categoria)

# -----------------------
# Eliminar categoría
# -----------------------

@main_bp.route('/categorias/eliminar/<int:id>', methods=['GET'])
def eliminar_categoria(id):
    categoria = Categoria.query.get_or_404(id)

    # Validar si hay productos asociados antes de eliminar
    if categoria.productos:  # Asumiendo que tienes una relación backref en Producto
        flash('No se puede eliminar la categoría porque tiene productos asociados.', 'error')
        return redirect(url_for('main_bp.listar_categorias'))

    db.session.delete(categoria)
    db.session.commit()
    flash('Categoría eliminada correctamente.')
    return redirect(url_for('main_bp.listar_categorias'))



# ------------------------
# Productos
# ------------------------
@main_bp.route('/productos')
def listar_productos():
    productos = Producto.query.all()
    return render_template('productos/listar.html', productos=productos)

@main_bp.route('/productos/nuevo', methods=['GET', 'POST'])
def nuevo_producto():
    form = ProductoForm()
    form.categoria.choices = [(c.id, c.nombre) for c in Categoria.query.all()]
    
    if form.validate_on_submit():

         # Aquí imprimimos el valor de la categoría seleccionada
        print("Categoría seleccionada:", form.categoria.data)

        producto = Producto(
            nombre=form.nombre.data,
            descripcion=form.descripcion.data,
            precio=form.precio.data,
            stock=form.stock.data,
            categoria_id=form.categoria.data
        )
        db.session.add(producto)
        db.session.commit()
        flash('Producto agregado exitosamente.')
        return redirect(url_for('main_bp.listar_productos'))
    
    return render_template('productos/nuevo.html', form=form)

# -----------------------
# Editar productos
# -----------------------
@main_bp.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    producto = Producto.query.get_or_404(id)
    form = ProductoForm(obj=producto)
    form.categoria.choices = [(c.id, c.nombre) for c in Categoria.query.all()]

    if form.validate_on_submit():
        producto.nombre = form.nombre.data
        producto.descripcion = form.descripcion.data
        producto.precio = form.precio.data
        producto.stock = form.stock.data
        producto.categoria_id = form.categoria.data

        db.session.commit()
        flash('Producto actualizado correctamente.')
        return redirect(url_for('main_bp.listar_productos'))

    return render_template('productos/nuevo.html', form=form, producto=producto)

# -----------------------
# Eliminar  productos
# -----------------------

@main_bp.route('/productos/eliminar/<int:id>', methods=['GET'])
def eliminar_producto(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    flash('Producto eliminado correctamente.')
    return redirect(url_for('main_bp.listar_productos'))


# ------------------------
# Ventas
# ------------------------

#@main_bp.route('/ventas/nueva', methods=['GET', 'POST'])
#def nueva_venta():
#    form = VentaForm()
#    if form.validate_on_submit():
#        producto = Producto.query.get(form.producto.data)
#        cantidad = form.cantidad.data
#        total = producto.precio * cantidad
        
        # Crear una nueva venta
#        venta = Venta(
#            total=total,
#            estado=form.estado.data,

        # Asignar productos a la venta
 #       venta.productos.append(producto)

        # Actualizar el stock
  #      producto.stock -= cantidad

   #     db.session.add(venta)
    #    db.session.commit()

     #   flash('Venta registrada con éxito.')
      #  return redirect(url_for('main_bp.listar_ventas'))

#    return render_template('ventas/nueva.html', form=form)

@main_bp.route('/ventas')
def listar_ventas():
    ventas = Venta.query.all()
    return render_template('ventas/listar.html', ventas=ventas)

# -----------------------
# Eliminar venta
# -----------------------

@main_bp.route('/ventas/eliminar/<int:id>', methods=['GET'])
def eliminar_venta(id):
    venta = Venta.query.get_or_404(id)

   
    #for producto in venta.productos:
       # producto.stock += venta_productos.cantidad  

    db.session.delete(venta)
    db.session.commit()
    flash('Venta eliminada correctamente.')
    return redirect(url_for('main_bp.listar_ventas'))


#################
    #LOGIN
#################

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Buscar el usuario por nombre de usuario
        usuario = Usuario.query.filter_by(username=form.username.data).first()

        # Verificar que el usuario existe y la contraseña es correcta
        if usuario and usuario.check_password(form.password.data):
            login_user(usuario)  # Esto maneja la sesión automáticamente
            flash('Sesión iniciada correctamente.', 'success')
            return redirect(url_for('dashboard'))  # Redirigir a la página protegida (ej. dashboard)
        else:
            flash('Nombre de usuario o contraseña incorrectos.', 'danger')
    
    return render_template('login.html', form=form)


@main_bp.route('/logout')
@login_required
def logout():
    logout_user()  # Usar logout_user de Flask-Login para cerrar la sesión
    flash('Sesión cerrada correctamente.', 'info')
    return redirect(url_for('main_bp.login'))


# -------------------
# RUTA PROTEGIDA 
# -------------------

#@main_bp.route('/dashboard')
#@login_required
#def dashboard():
  #  return render_template('dashboard.html')  # Página protegida que solo los usuarios logueados pueden ver


from app.fraude.modelos_fraude import predecir_fraude
from flask import request

@main_bp.route('/ventas/nueva', methods=['GET', 'POST'])
def nueva_venta():
    form = VentaForm()
    if form.validate_on_submit():
        producto = Producto.query.get(form.producto.data)
        cantidad = form.cantidad.data
        total = producto.precio * cantidad

        metodo_pago = form.metodo_pago.data

        # 👉 Aquí usamos el modelo de IA solo si el método es tarjeta
        if metodo_pago == 'tarjeta':
            transacciones_previas = 3  # puedes ajustar este valor si lo cuentas de la base de datos
            categoria_nombre = producto.categoria.nombre  # asegurándote de que producto tiene categoría relacionada

            resultado = predecir_fraude(total, transacciones_previas, categoria_nombre)
            flash(f'Validación de tarjeta: {resultado}')

            if "fraude" in resultado.lower():
                flash('Transacción cancelada por posible fraude.', 'danger')
                return redirect(url_for('main_bp.nueva_venta'))

        # Si no hay fraude, o es efectivo, continuar con la venta normal
        venta = Venta(
            total=total,
            estado=form.estado.data,
        )
        venta.productos.append(producto)
        producto.stock -= cantidad  # actualizar stock

        db.session.add(venta)
        db.session.commit()

        flash('Venta registrada correctamente.', 'success')
        return redirect(url_for('main_bp.listar_ventas'))

    return render_template('ventas/nueva.html', form=form)
