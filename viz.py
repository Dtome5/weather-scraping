import h5py
import polars as pl
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import openmeteo_requests
import requests_cache
from retry_requests import retry
from matplotlib.collections import LineCollection
from datetime import datetime, timedelta

"""
cache_session = requests_cache.CachedSession(".cache", expire_after=-1)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)
url = "https://archive-api.open-meteo.com/v1/archive"

params = {
    "latitude": 52.52,
    "longitude": 13.41,
    "start_date": "2024-12-27",
    "end_date": "2025-01-10",
    "daily": "temperature_2m_mean",
    "temporal_resolution": "hourly_6",
}

responses = openmeteo.weather_api(url, params=params)
response = responses[0]
daily = response.Daily()
daily_temperature_2m_mean = daily.Variables(0).ValuesAsNumpy()

daily_data = {
    "date": pd.date_range(
        start=pd.to_datetime(daily.Time(), unit="s", utc=True),
        end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=daily.Interval()),
        inclusive="left",
    )
}

daily_data["temperature_2m_mean"] = daily_temperature_2m_mean

daily_dataframe = pd.DataFrame(data=daily_data)
print(daily_dataframe)
"""

webpages = pl.read_csv("websites.csv")
locations = webpages.get_column("Location")
data = h5py.File("weather.hdf5", "r")
today = datetime.now().date()
yesterday = today - timedelta(1)
twoda = today - timedelta(2)

df = pl.DataFrame(
    {
        "date": [today - timedelta(x) for x in range(99)],
        "locations": [
            "Abuja",
            "Bad Honeff",
            "London",
        ]
        * 33,
        "Temperature": np.random.uniform(20, 40, 99),
        "Humidity": np.random.uniform(40, 70, 99),
        "Wind Speed": np.random.uniform(5, 15, 99),
    }
)

# print(pd.read_hdf("weather2.hdf5"))
df2 = pl.read_csv("/home/dtome/Code/Python/WebScraping/open-meteo-52.55N13.41E38m.csv")
print(df2)

abuja = df.filter(pl.col("locations") == "Abuja")
bh = df.filter(pl.col("locations") == "Bad Honeff")
london = df.filter(pl.col("locations") == "London")

fig1, ax = plt.subplots(figsize=(6, 4))
arr = np.array([1, 2, 3, 4, 4, 3, 2, 1])
ax.plot(abuja.select(pl.col("Temperature")).to_series())
ax.plot(bh.select(pl.col("Temperature")).to_series())
ax.plot(london.select(pl.col("Temperature")).to_series())
fig1.savefig("plot.png")

fig2, ax2 = plt.subplots(figsize=(8, 5))
cols = df2.columns
col1 = df2[cols[1]]
ax2.plot(col1)
fig2.savefig("plot2.png")
