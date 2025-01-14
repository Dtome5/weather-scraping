import h5py

# from matplotlib import axes, figure
# from pandas.core.frame import Axes
from pandas.core.tools.datetimes import DatetimeScalar
import polars as pl
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
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

abuja = df.filter(pl.col("locations") == "Abuja")
bh = df.filter(pl.col("locations") == "Bad Honeff")
london = df.filter(pl.col("locations") == "London")


# print(pd.read_hdf("weather2.hdf5"))
df2 = pl.read_csv(
    "/home/dtome/Code/Python/WebScraping/open-meteo-9.03N7.47E480mabuja.csv",
    skip_rows=3,
)
df3 = pl.read_csv(
    "/home/dtome/Code/Python/WebScraping/open-meteo-50.65N7.18E77mBadHonnef.csv",
    skip_rows=3,
)
df4 = pl.read_csv(
    "/home/dtome/Code/Python/WebScraping/open-meteo-51.49N0.16W23mlondon.csv",
    skip_rows=3,
)
print(df2)


fig, ax = plt.subplots(figsize=(8, 5))
fig2, ax2 = plt.subplots(figsize=(8, 5))
fig3, ax3 = plt.subplots(figsize=(8, 5))

dataframes = [df2, df3, df4]


def plot_vals(dfs, col, figname):
    fig, ax = plt.subplots(figsize=(8, 5))
    for df in dfs:
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
        ax.plot(df[:, 0].str.strptime(pl.Datetime, format="%Y-%m-%dT%H:%M"), df[:, col])
        ax.set_xlabel(f"{df.columns[col]}")
    fig.savefig(f"{figname}.png")


print(df2[:, 0].str.strptime(pl.Date, format="%Y-%m-%dT%H:%M"))
df5 = df2.__copy__()
df5 = df5.replace_column(0, df5[:, 0].str.strptime(pl.Date, format="%Y-%m-%dT%H:%M"))
print(df5.group_by(df5[:, 0]).agg(pl.col(df5.columns[1]).mean()))
plot_vals(dataframes, 1, "plt1")
# plot_vals(df2, 1, "plot3.png")
# plot_vals(df3, 1, "plot3.png")
# plot_vals(df4, 1, "plot3.png")
# plot_vals(df2, 2, "plot4.png")
# plot_vals(df3, 2, "plot4.png")
# plot_vals(df4, 2, "plot4.png")
# plot_vals(df2, 4, "plot5.png")
# plot_vals(df3, 4, "plot5.png")
# plot_vals(df4, 4, "plot5.png")
