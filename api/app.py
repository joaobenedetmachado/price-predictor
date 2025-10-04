import tensorflow as tf
import tensorflow_decision_forests as tfdf
import numpy as np
import csv
from fastapi import FastAPI, File, UploadFile
import pandas as pd 
from datetime import date, timedelta

app = FastAPI()

df = pd.DataFrame()

import tensorflow_decision_forests as tfdf
import pandas as pd

import pandas as pd
import tensorflow_decision_forests as tfdf

def split_train_test(df):
    df["Date"] = pd.to_datetime(df["Date"])

    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["Day"] = df["Date"].dt.day

    df = df.drop(columns=["Date"])

    dataset = tfdf.keras.pd_dataframe_to_tf_dataset(df, label="Price")

    for features, label in dataset.take(5):
        print("Features:", features)
        print("Label:", label.numpy())



def return_pridictions(data, range_values):
    data = data.drop_duplicates()
    data["Date"] = pd.to_datetime(data["Date"])
    last_date = data["Date"].max()
    future_dates = [last_date + timedelta(days=i) for i in range(1, range_values + 1)] # increment 1 by 1 to show the future dates
    
    split_train_test(data)
    # value_predicted = predict_by_range(test, train, range)
    # ruturn value_predicted    
    
    return future_dates



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