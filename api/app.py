import tensorflow as tf
import tensorflow_decision_forests as tfdf
from sklearn.model_selection import train_test_split
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

def prepare_data(df):
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["Day"] = df["Date"].dt.day

    df = df.drop(columns=["Date"])

    dataset = tfdf.keras.pd_dataframe_to_tf_dataset(df, label="Price")

    for features, label in dataset.take(5):
        print("Features:", features)
        print("Label:", label.numpy())

    X = df.drop(columns=['Price'])
    y = df['Price']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    return X_train, X_test, y_train, y_test

def return_pridictions(data, range_values):
    data = data.drop_duplicates()
    data["Date"] = pd.to_datetime(data["Date"])
    
    X_train, X_test, y_train, y_test = prepare_data(data)
    value_predicted = predict_by_range(X_train, X_test, y_train, y_test, range_values, data)
    
    return value_predicted

def predict_by_range(X_train, X_test, y_train, y_test, range, data):
    X_train = tf.convert_to_tensor(X_train, dtype=tf.float32)
    X_test = tf.convert_to_tensor(X_test, dtype=tf.float32)
    y_train = tf.convert_to_tensor(y_train, dtype=tf.float32)
    y_test = tf.convert_to_tensor(y_test, dtype=tf.float32)

    model = tf.keras.Sequential([
        tf.keras.layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(1)
    ])

    model.compile(optimizer="adam", loss='mse', metrics=["mae"])

    model.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test))

    last_date = pd.to_datetime(data["Date"].iloc[-1])
    future_dates = pd.date_range(last_date + pd.Timedelta(days=1), periods=range)

    future_df = pd.DataFrame({
        "Year": future_dates.year,
        "Month": future_dates.month,
        "Day": future_dates.day,
    })

    X_future = tf.convert_to_tensor(future_df, dtype=tf.float32)

    predictions = model.predict(X_future).flatten()

    return pd.DataFrame({
        "Date": future_dates,
        "PredictedPrice": predictions
    }).to_dict(orient="records")


@app.post("/predict")
async def predict(range_values: int, file: UploadFile = File(...)):
    df = pd.read_csv(file.file)
    if "Price" not in df.columns or "Date" not in df.columns:
        return {"error": "CSV must contain 'Price' and 'Date' columns."}

    return_values = return_pridictions(df, range_values)

    return return_values