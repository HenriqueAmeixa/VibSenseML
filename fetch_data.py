import requests
import polars as pl
from datetime import datetime
from config import API_URL, DEVICE_ID, LIMIT

def get_sensor_data(after_id=None):
    params = {"limit": LIMIT}
    if after_id is not None:
        params["afterId"] = after_id

    url = f"{API_URL}/{DEVICE_ID}"
    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()
    if not data:
        return pl.DataFrame()

    return pl.DataFrame(data)
