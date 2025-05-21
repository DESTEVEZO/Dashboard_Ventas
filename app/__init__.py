from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # <-- Asegúrate de importar esto

db = SQLAlchemy()
migrate = Migrate()  # <-- Instancia Migrate

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'tu-clave-secreta'
    
    # Aquí reemplazamos la URI de SQLite por la URI de MySQL
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Admin.2025@localhost/dashboard_ventas'  # <-- Cambia la URI aquí
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)  # <-- Importante para que funcione flask db

    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app
