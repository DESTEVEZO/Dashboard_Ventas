# forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, FloatField, IntegerField, SelectField, PasswordField
from wtforms.validators import DataRequired
from app.models import Producto

# -------------------------
# Formulario para Categoría
# -------------------------

class CategoriaForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    descripcion = TextAreaField('Descripción')
    estado = BooleanField('Activo', default=True)
    submit = SubmitField('Guardar')

# -------------------------
# Formulario para Producto
# -------------------------

class ProductoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    descripcion = TextAreaField('Descripción')
    precio = FloatField('Precio', validators=[DataRequired()])
    stock = IntegerField('Stock', validators=[DataRequired()])
    categoria = SelectField('Categoría', coerce=int)
    submit = SubmitField('Guardar')

# -------------------------
# Formulario para Venta
# -------------------------

class VentaForm(FlaskForm):
    producto = SelectField('Producto', coerce=int, validators=[DataRequired()])
    cantidad = IntegerField('Cantidad', validators=[DataRequired()])
    estado = SelectField('Estado', choices=[
        ('Pagada', 'Pagada'),
        ('Pendiente', 'Pendiente'),
        ('Cancelada', 'Cancelada')
    ], validators=[DataRequired()])

    metodo_pago = SelectField('Método de Pago', choices=[
        ('tarjeta', 'Tarjeta'),
        ('efectivo', 'Efectivo'),
        ('transferencia', 'Transferencia')
    ], validators=[DataRequired()])

    submit = SubmitField('Registrar Venta')

    def __init__(self, *args, **kwargs):
        super(VentaForm, self).__init__(*args, **kwargs)
        self.producto.choices = [(producto.id, producto.nombre) for producto in Producto.query.all()]


# -------------------------
# Formulario para login
# -------------------------


class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar Sesión')
