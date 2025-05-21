from app import db
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    descripcion = db.Column(db.String(255))
    estado = db.Column(db.Boolean, default=True)  # Activo o desactivado lógicamente

    def __repr__(self):
        return f'<Categoria {self.nombre}>'
    

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    descripcion = db.Column(db.String(255))
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    categoria = db.relationship('Categoria', backref=db.backref('productos', lazy=True))

    def __repr__(self):
        return f'<Producto {self.nombre}>'


# Tabla intermedia para productos vendidos en una venta
venta_producto = db.Table('venta_producto',
    db.Column('venta_id', db.Integer, db.ForeignKey('venta.id')),
    db.Column('producto_id', db.Integer, db.ForeignKey('producto.id'))
)

from datetime import datetime

class Venta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, default=datetime.utcnow)
    total = db.Column(db.Float)
    estado = db.Column(db.String(50))  # Pagada, Pendiente, Cancelada
    metodo_pago = db.Column(db.String(20), nullable=False, default='efectivo')  # Nuevo campo

    # Relación muchos a muchos con productos
    productos = db.relationship('Producto', secondary=venta_producto, lazy='subquery')

    def __repr__(self):
        return f'<Venta {self.id} - Total: {self.total} - Pago: {self.metodo_pago}>'

    
#################################
        #Login
#################################

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Usuario {self.username}>'


