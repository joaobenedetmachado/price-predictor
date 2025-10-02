import tensorflow as tf
import csv
from fastapi import FastAPI, File, UploadFile
import pandas as pd 

app = FastAPI()

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)
    print(df.head())
    return {"actual": df["Price"].tolist(), "predicted": df["Price"].tolist()}
    
