import tensorflow as tf
import csv
import fastapi
import pandas as pd 

app = fastapi.FastAPI()

@app.post("/dataset")
def create_dataset(file_path: str):
    data = pd.read_csv(file_path)
    dataset = tf.data.Dataset.from_tensor_slices(dict(data))
    return dataset