import polars as pl
import matplotlib.pyplot as plt
import requests

url = "https://apisensor.azurewebsites.net/api/SensorReadings/device/f68fb3dd-65b9-47c3-b638-1bad36be5e37"
headers = {
    "x-api-key": "abc123secretapikeyxyz"
}

response = requests.get(url, headers=headers)
if response.status_code != 200:
    raise Exception(f"Erro ao buscar dados: {response.status_code}")

dados = response.json()
df = pl.from_dicts(dados)

# Converte os dados para listas
timestamps = df["timestamp"].to_list()
x = df["accelX"].to_list()
y = df["accelY"].to_list()
z = df["accelZ"].to_list()

# Plota os três eixos
plt.figure(figsize=(14, 6))
plt.plot(timestamps, x, label="accelX")
plt.plot(timestamps, y, label="accelY")
plt.plot(timestamps, z, label="accelZ")

plt.xlabel("Timestamp")
plt.ylabel("Aceleração (g)")
plt.title("Gráfico de Aceleração nos 3 Eixos")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
