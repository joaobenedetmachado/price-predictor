import tensorflow as tf
import csv
from fastapi import FastAPI, File, UploadFile
import pandas as pd 
from datetime import date, timedelta

app = FastAPI()

df = pd.DataFrame()

@app.post("/predict")
async def predict(range_values: int, file: UploadFile = File(...)):
    df = pd.read_csv(file.file)
    if "Price" not in df.columns or "Date" not in df.columns:
        return {"error": "CSV must contain 'Price' and 'Date' columns."}

    return_values = return_pridictions(df, range_values)

    return_formated_values = []
    for i in return_values:
        return_formated_values.append(str(i)[:10])  

    return return_formated_values

def return_pridictions(data, range_values):
    data = data.drop_duplicates()
    data["Date"] = pd.to_datetime(data["Date"])
    last_date = data["Date"].max()
    future_dates = [last_date + timedelta(days=i) for i in range(1, range_values + 1)] # increment 1 by 1 to show the future dates
    return future_dates
