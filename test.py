import requests

url = "http://127.0.0.1:8000/predict"
params = {"range_values": 5}

with open("/home/joao/price-predictor/api/data-test/data.csv", "rb") as f:
    files = {"file": ("/home/joao/price-predictor/api/data-test/data.csv", f, "text/csv")}
    response = requests.post(url, params=params, files=files)

print("Status:", response.status_code)
print("Resposta JSON:", response.json())
