from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

# Load the trained model
model = joblib.load("model.pkl")

# Create FastAPI app
app = FastAPI()

# Input schema
class PatientData(BaseModel):
    Age: int
    Sex: int
    ChestPainType: int
    RestingBP: int
    Cholesterol: int
    FastingBS: int
    RestingECG: int
    MaxHR: int
    ExerciseAngina: int
    Oldpeak: float
    ST_Slope: int

# Test route
@app.get("/")
def home():
    return {"message": "Heart Disease Diagnosis API is live 🚀"}

# Predict route with custom threshold
@app.post("/predict")
def predict(data: PatientData):
    # Step 1: Prepare input for model
    input_data = np.array([[ 
        data.Age, data.Sex, data.ChestPainType, data.RestingBP, 
        data.Cholesterol, data.FastingBS, data.RestingECG, 
        data.MaxHR, data.ExerciseAngina, data.Oldpeak, data.ST_Slope
    ]])

    # Step 2: Predict probability of heart disease (class = 1)
    probability = model.predict_proba(input_data)[0][1]

    # Step 3: Apply custom threshold
    threshold = 0.4
    prediction = int(probability > threshold)

    # Step 4: Build response
    result = {
        "prediction": prediction,
        "has_heart_disease": bool(prediction),
        "probability": round(probability, 3),
        "threshold_used": threshold,
        "message": "⚠️ High risk of Heart Disease" if prediction else "💖 Low risk of Heart Disease"
    }

    return result
