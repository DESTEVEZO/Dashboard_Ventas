# entrenar_modelos_fraude.py

import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.model_selection import train_test_split

# Crear datos ficticios
np.random.seed(42)

# Generar datos
monto = np.random.normal(loc=50, scale=20, size=1000)  # montos de transacciones
transacciones = np.random.randint(1, 10, 1000)  # número de transacciones previas
categorias = np.random.choice(['Electrónica', 'Ropa', 'Hogar', 'Alimentos'], 1000)
fraude = np.random.choice([0, 1], 1000, p=[0.95, 0.05])  # solo 5% de fraude

# Crear DataFrame
df = pd.DataFrame({
    'monto': monto,
    'transacciones': transacciones,
    'categoria': categorias,
    'fraude': fraude
})

# One-hot encoding para la columna 'categoria'
df = pd.get_dummies(df, columns=['categoria'])

# Separar features y etiqueta
X = df.drop('fraude', axis=1)
y = df['fraude']

# Entrenar modelo Random Forest (supervisado)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Entrenar modelo Isolation Forest (no supervisado)
iso_model = IsolationForest(contamination=0.05, random_state=42)
iso_model.fit(X)

# Guardar los modelos
joblib.dump(rf_model, 'random_forest_model.pkl')
joblib.dump(iso_model, 'isolation_forest_model.pkl')

print(" Modelos entrenados y guardados como .pkl correctamente.")
