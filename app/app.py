import streamlit as st
import requests

# Titulo de la aplicacion
st.title("Predicción de Diabetes")

# Introduccion a la aplicacion
st.write("""
Esta aplicación predice si un paciente puede tener diabetes o no, basándose en los siguientes datos:
- Número de embarazos (Pregnancies)
- Nivel de glucosa (Glucose)
- Presión arterial (BloodPressure)
- Grosor de la piel (SkinThickness)
- Nivel de insulina (Insulin)
- Índice de masa corporal (BMI)
- Función del pedigrí de diabetes (DiabetesPedigreeFunction)
- Edad (Age)
""")

# Entrada de datos
st.header("Ingresa los datos del paciente")

# Campos de entrada
pregnancies = st.number_input("Número de embarazos (Pregnancies)", min_value=0, value=0)
glucose = st.number_input("Nivel de glucosa (Glucose)", min_value=0, value=0)
blood_pressure = st.number_input("Presión arterial (BloodPressure)", min_value=0, value=0)
skin_thickness = st.number_input("Grosor de la piel (SkinThickness)", min_value=0, value=0)
insulin = st.number_input("Nivel de insulina (Insulin)", min_value=0, value=0)
bmi = st.number_input("Índice de masa corporal (BMI)", min_value=0.0, value=0.0)
age = st.number_input("Edad (Age)", min_value=0, value=0)

# Campo para ingresar Diabetes Pedigree Function manualmente si se conoce
st.subheader("Función del Pedigrí de Diabetes")
diabetes_pedigree_manual = st.number_input(
    "Ingresa el valor de Diabetes Pedigree Function (si lo conoces):",
    min_value=0.0,
    value=0.0,
    step=0.0001,
    format="%.4f"
)

# Historia familiar para calcular Diabetes Pedigree Function
st.subheader("Si no conoce el valor de la funcion rellene la Historia Familiar de Diabetes")
father_diabetes = st.checkbox("Padre tiene diabetes")
mother_diabetes = st.checkbox("Madre tiene diabetes")
sibling_diabetes = st.checkbox("Hermano tiene diabetes")
grandparent_diabetes = st.checkbox("Abuelos tienen diabetes")

# Calculamos la Diabetes Pedigree Function si no se ingresa manualmente
if diabetes_pedigree_manual != 0.0:
    diabetes_pedigree = diabetes_pedigree_manual  # Usar el valor manual
else:
    # Calculamos automaticamente basado en la historia familiar
    diabetes_pedigree = 0.0
    if father_diabetes:
        diabetes_pedigree += 0.3
    if mother_diabetes:
        diabetes_pedigree += 0.3
    if sibling_diabetes:
        diabetes_pedigree += 0.1
    if grandparent_diabetes:
        diabetes_pedigree += 0.2
    if diabetes_pedigree == 0.0:
        diabetes_pedigree = 0.3725  # Valor de la mediana si no hay historia familiar

# Mostramos el valor de Diabetes Pedigree Function
st.write(f"Valor de Diabetes Pedigree Function: **{diabetes_pedigree:.4f}**")

# Al dar este boton realizamos la prediccion llamando a la API
if st.button("Predecir"):
    # Creamos el diccionario de datos
    data = {
        "Pregnancies": pregnancies,
        "Glucose": glucose,
        "BloodPressure": blood_pressure,
        "SkinThickness": skin_thickness,
        "Insulin": insulin,
        "BMI": bmi,
        "DiabetesPedigreeFunction": diabetes_pedigree,
        "Age": age,
    }

    # Enviamos la solicitud al API
    response = requests.post("http://localhost:8000/predict", json=data)

    # Mostramos la prediccion y la confianza
    if response.status_code == 200:
        result = response.json()
        prediction = result["prediction"]
        probability = result["probability"] * 100  # Convertimos a porcentaje

        if prediction == 1:
            st.error(f"El paciente tiene riesgo de diabetes. (Probabilidad de la Prediccion: {probability:.2f}%)")
        else:
            st.success(f"El paciente no tiene riesgo de diabetes. (Probabilidad de la Prediccion: {probability:.2f}%)")
    else:
        st.error("Error al obtener la predicción. Por favor, verifica los datos ingresados.")
    
    