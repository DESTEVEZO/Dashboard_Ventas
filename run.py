from app import create_app, db

app = create_app()

# Crear las tablas en la base de datos al iniciar la app
with app.app_context():
    db.create_all()  # Crea las tablas si no existen

if __name__ == '__main__':
    app.run(debug=True)
