import h5py
import polars as pl
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from pandas.core.tools.datetimes import DatetimeScalar
from matplotlib.collections import LineCollection
from datetime import datetime, timedelta


webpages = pd.read_csv("websites.csv")
locations = webpages["Location"]
data = h5py.File("weather.hdf5", "r")
today = datetime.now().date()
df = pd.DataFrame(
    {
        "time": [today - timedelta(x) for x in range(99)],
        "Temperature": np.random.uniform(20, 40, 99),
        "Humidity": np.random.uniform(40, 70, 99),
        "Wind Speed": np.random.uniform(5, 15, 99),
    }
)


fig, ax = plt.subplots(figsize=(8, 5))
fig2, ax2 = plt.subplots(figsize=(8, 5))
fig3, ax3 = plt.subplots(figsize=(8, 5))
websites = pd.read_csv("websites.csv")
dataframes = [
    pd.read_hdf("weather3.hdf5", key=websites["Location"][i])
    for i in range(websites.shape[0])
]
print(dataframes[1])


def plot_vals(dfs, col, figname):
    fig, ax = plt.subplots(figsize=(8, 5))
    for df in dfs:
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
        ax.plot(pd.to_datetime(df.iloc[:, 0], format="%Y-%m-%d"), df.iloc[:, col])
        ax.set_xlabel(f"{df.columns[col]}")
    fig.savefig(f"{figname}.png")


def plot_loc(dfs, figname):
    fig, ax = plt.subplots()
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=10))
    for df in dfs:
        times = pd.to_datetime(df.iloc[:, 0], format="%Y-%m-%d")
        ax.plot(times, df.iloc[:, 1])
        ax.plot(times, df.iloc[:, 2])
        ax.plot(times, df.iloc[:, 3])
        # ax.set_label(df.columns)
        ax.set_xlabel(f"{df.columns[0]}")
        ax.legend(df.columns[1:])
    fig.savefig(f"{figname}")


plot_vals(dataframes, 1, "plt1")
plot_loc([df, df, df], "new.png")
