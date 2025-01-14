import requests
import h5py
import pandas as pd
import polars as pl
import re
import json
import urllib.request
import numpy as np

# import pyarrow as pa
from datetime import datetime, timedelta
from bs4 import BeautifulSoup as bs
from requests.models import LocationParseError


def to_num(var: str):
    new_val = ""
    for i in var:
        if i.isnumeric() == True:
            new_val += i
    return int(new_val)


def get_temp(soup: bs):
    val = soup.find("div", {"class", "current-temp"})
    return val.text


def get_humidity(soup: bs):
    val = soup.find("lib-display-unit", {"type": "humidity"})
    return val.text


def get_loc(soup: bs):
    val = soup.find("strong", {"class": "location-data"})
    return val.text


def get_wind_speed(soup: bs):
    val = soup.find("header", {"class": "wind-speed"})
    return val.text


def gettmpavg():
    soup = bs(
        requests.get("https://weather.com/en-NG/weather/today/l/NIXX0022:1:NI").content,
        "html.parser",
    )

    val = soup.find("span", {"class", "Wind--windWrapper--NsCjc undefined"})
    val2 = soup.find("span", {"class", "CurrentConditions--tempValue--zUBSz"})
    hum = soup.select_one(
        "div.ListItem--listItem--UuEqg:nth-child(3) > div:nth-child(3) > span:nth-child(1)"
    )

    temp = soup.select_one(".CurrentConditions--tempValue--zUBSz")
    print(val.span.name, val2.text, hum.text, temp.text)


def getnoaa():
    soup = bs(
        requests.get("https://www.weather.gov/wrh/Climate?wfo=maf").content,
        "html.parser",
    )

    val = soup.select_one(".tablesorter")
    print(val)


def append_hdf5(group, dataset, obj):
    data = np.array([obj], dtype="i")
    if dataset not in group:
        group.create_dataset(dataset, data=data, maxshape=(None,), chunks=True)
    else:
        group[dataset].resize((group[dataset].shape[0] + len(data),))
        group[dataset][-len(data) :] = data


def pl_to_hdf5(df, filepath):
    file = h5py.File(filepath, mode="a")
    cols = df.columns
    for col in cols:
        print(col)
        dset = file.create_dataset(
            col, shape=(None,), dtype=df[col].dtype, data=df[col], chunks=True
        )


def hdf5_to_pl(filepath: str, k=None) -> pl.DataFrame:
    file = h5py.File(filepath, mode="r+")
    dictionary = {}
    if k:
        file = file[k]
    keys = file.keys()
    for key in keys:
        print(f"keys is {key}")
        dictionary[key] = list(file[key])
    df = pl.DataFrame(dictionary)
    return df


def load_to_hdf5(location, temperature, humidity, wind_speed):
    for i in len(temperature):
        df = pl.DataFrame(
            {
                "temperature": temperature[i],
                "humidity": humidity[i],
                "wind speed": wind_speed[i],
            }
        )
        pl_to_hdf5(df, filepath, location[i])


# getnoaa()
# gettmpavg()
"""
file = h5py.File("weather.hdf5", "a")
websites = pd.read_csv("websites.csv")
today = (datetime.now() - timedelta(4)).date().strftime("%y-%m-%d")
urls = [websites["URL"][i] + f"/date/{today}" for i in range(len(websites))]
pages = [requests.get(url) for url in urls]
scraped_pages = [bs(page.content, "html.parser") for page in pages]
temperature = [get_temp(scraped_page) for scraped_page in scraped_pages]
humidity = [get_humidity(scraped_page) for scraped_page in scraped_pages]
temperature = [to_num(temp) for temp in temperature]
humidity = [to_num(hum) for hum in humidity]
locations = [get_loc(scraped_page) for scraped_page in scraped_pages]
wind_speeds = [get_wind_speed(scraped_page) for scraped_page in scraped_pages]
df = pd.DataFrame(
    data={
        "Date": today,
        "Location": locations,
        "Temperature": temperature,
        "Humidity": humidity,
        "Wind_speeds": wind_speeds,
    }
)
"""
df = pd.DataFrame(
    data={
        "location": ["Abuja"],
        "Temperature": [30],
        "Humidity": [30],
        "Wind Speeds": [10],
    }
)
print(df)
df.to_hdf(path_or_buf="weather2.hdf5", key=df.iloc[0, 0])
print(hdf5_to_pl("weather.hdf5", k="Lagos, Lagos, Nigeria"))
file2 = h5py.File("weather2.hdf5", "r")
print(list(file2[df.iloc[0, 0]]))
# for i in scraped_pages:
# print(
#     file[locations[0]]["temperature"][:],
#     file[locations[0]]["humidity"][:],
#     file[locations[0]]["wind_speeds"][:],
# )
# for loc in range(len(locations)):
#     if locations[loc] not in file.keys():
#         group = file.create_group(locations[loc])
#     group = file[locations[loc]]
#     data = [temperature, humidity, wind_speeds]
#     data_str = ["temperature", "humidity", "wind_speeds"]
#     for d in range(len(data)):
#         append_hdf5(group, data_str[d], data[d][loc])
# print(group[data_str[d]])

# file.close()
