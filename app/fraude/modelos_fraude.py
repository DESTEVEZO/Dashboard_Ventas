# fraude/modelos.py
import joblib

# Cargar los modelos entrenados (asegúrate de tener los archivos .pkl en el directorio adecuado)
rf_model = joblib.load('random_forest_model.pkl')
iso_forest = joblib.load('isolation_forest_model.pkl')

def predecir_fraude(monto, numero_transacciones, categoria_producto):
    # Codificar la categoría del producto
    categoria_encoded = {'Electrónica': 0, 'Ropa': 1, 'Hogar': 2, 'Alimentos': 3}
    categoria_num = categoria_encoded.get(categoria_producto, -1)

    # Formar el vector de características
    datos = [[monto, numero_transacciones, categoria_num]]

    # Realizar las predicciones con ambos modelos
    prediccion_rf = rf_model.predict(datos)
    prediccion_iso = iso_forest.predict(datos)

    # Evaluar el resultado
    if prediccion_rf == 1 or prediccion_iso == -1:
        return "Posible fraude detectado"
    else:
        return "Transacción segura"
