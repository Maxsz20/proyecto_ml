from fastapi import FastAPI, HTTPException
import joblib
import pandas as pd
from sklearn.preprocessing import StandardScaler

app = FastAPI()

# Cargamos el modelo entrenado
model = joblib.load("modelo_logistic_regression.pkl")

# Cargamos el scaler
scaler = joblib.load("scaler.pkl")

column_names = [
    "Pregnancies",
    "Glucose",
    "BloodPressure",
    "SkinThickness",
    "Insulin",
    "BMI",
    "DiabetesPedigreeFunction",
    "Age",
]

# Ruta raiz
@app.get("/")
async def root():
    return {"message": "Bienvenido al API de predicción de diabetes. Accede a /docs para ver la documentación."}

# Ruta de prediccion
@app.post("/predict")
async def predict(data: dict):
    try:
        # Obtenemos los datos del usuario
        input_data = [
            data.get("Pregnancies"),
            data.get("Glucose"),
            data.get("BloodPressure"),
            data.get("SkinThickness"),
            data.get("Insulin"),
            data.get("BMI"),
            data.get("DiabetesPedigreeFunction"),
            data.get("Age"),
        ]

        # Convertimos los datos en un DataFrame de pandas
        input_df = pd.DataFrame([input_data], columns=column_names)

        # Seleccionamos las variables a escalar
        features_to_scale = ['Glucose', 'BloodPressure', 'Age', 'Insulin', 'BMI', 'SkinThickness']

        # Aplicamos el scaler a las variables seleccionadas
        input_df[features_to_scale] = scaler.transform(input_df[features_to_scale])

        # Hacemos la prediccion y obtenemos las probabilidades
        prediction = model.predict(input_df)
        probabilities = model.predict_proba(input_df)
        
        probability = probabilities[0][prediction[0]] # Obtenemos la probabilidad unicamente de la clase seleccionada

        print("Predicción:", prediction)

        # Devolvemos la prediccion y la probabilidad como respuesta a la app
        return {
            "prediction": int(prediction[0]),
            "probability": float(probability)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))