import h5py
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import sys
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
    pd.read_hdf("weather.hdf5", key=websites["Location"][i])
    for i in range(websites.shape[0])
]


def plot_vals(dfs):
    for i in range(dfs[0].shape[1]):
        fig, ax = plt.subplots(figsize=(8, 5))
        for df in dfs:
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
            ax.plot(
                pd.to_datetime(df.iloc[:, 0], format="%Y-%m-%d %H:%M"), df.iloc[:, i]
            )
            ax.set_ylabel(f"{df.columns[i]}")
            ax.legend(websites["Location"])
            # ax.tight_layout()
        fig.suptitle(
            f"Figure {i+3}: {str.title(df.columns[i]).replace("_"," ")} Trends Across London, Abuja and Bad Honnef",
            x=0,
            ha="left",
        )
        fig.savefig(f"{df.columns[i]}.png")


# def plot_param(df,param,fignum):
#     fig, ax = plt.subplots(figsize=(8, 5))
#     ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
#     ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
#     ax.plot(pd.to_datetime(df.iloc[:, 0], format="%Y-%m-%d"), df.iloc[:, i])
#     ax.set_ylabel(f"{df.columns[i]}")
#     ax.legend(websites["Location"])
#     # ax.tight_layout()
#     ax.set_title(f" {str.title(df.columns[i]).replace("_"," ")} Trends Across London, Abuja and Bad Honnef")
#     fig.savefig(f"{df.columns[i]}.png")

# def plot_loc(df,loc,fignum):
#     fig, ax = plt.subplots(figsize=(8,5))
#     ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
#     ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
#     times = pd.to_datetime(df.iloc[:, 0], format="%Y-%m-%d")
#     ax.plot(times, df.iloc[:, 1])
#     ax.plot(times, df.iloc[:, 2])
#     ax.plot(times, df.iloc[:, 3])
#     # ax.set_label(df.columns)
#     ax.set_ylabel(f"{str(loc).replace("_"," ")}")
#     ax.set_xlabel(f"{df.columns[0]}")
#     ax.legend(df.columns[1:])
#     ax.set_title(f"Weather parameters in {str(loc).replace("_"," ")}")
#     fig.savefig(f"{loc}.png")


def plot_locs(dfs):
    for i in range(len(dfs)):
        df = dfs[i]
        fig, ax = plt.subplots()
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
        times = pd.to_datetime(df.iloc[:, 0], format="%Y-%m-%d %H:%M")
        ax.plot(times, df.iloc[:, 1])
        ax.plot(times, df.iloc[:, 2])
        ax.plot(times, df.iloc[:, 3])
        # ax.set_label(df.columns)
        ax.set_ylabel(f"{str(websites["Location"][i]).replace("_"," ")}")
        ax.set_xlabel(f"{df.columns[0]}")
        ax.legend(df.columns[1:])
        ax.set_title(
            f"Figure {i+1}: Weather parameters in {str(websites["Location"][i]).replace("_"," ")}",
            loc="left",
        )
        fig.savefig(f"{websites["Location"][i]}.png")


plot_vals(dataframes)
plot_locs(dataframes)
def show():
    print(dataframes[1])

if len(sys.argv) > 1:
    if sys.argv[1] == "show":
        print(dataframes[1])
