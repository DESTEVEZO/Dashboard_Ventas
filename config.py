import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'mi_clave_secreta'  # Clave secreta para sesiones
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Desactivar modificaciones de seguimiento
    
    # Aquí reemplazamos la URI de SQLite por la URI de MySQL
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:Admin.2025@localhost/dashboard_ventas'
