import requests
import h5py
import pandas as pd
import re
import json
import urllib.request
import numpy as np

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
    # val = soup.find("div", {"class", "current-temp"})
    val = soup.select_one(".CurrentConditions--tempValue--zUBSz")
    return val.text


def get_humidity(soup: bs):
    # val = soup.find("lib-display-unit", {"type": "humidity"})
    val = soup.select_one(
        "div.WeatherDetailsListItem--WeatherDetailsListItem--HLP3I:nth-child(3) > div:nth-child(3) > span:nth-child(1)"
    )
    return val.text


def get_loc(soup: bs):
    # val = soup.find("strong", {"class": "location-data"})
    val = soup.select_one(".CurrentConditions--location--yub4l")
    return val.text


def get_wind_speed(soup: bs):
    val = soup.select_one(".Wind--windWrapper--NsCjc > span:nth-child(2)")
    # val = soup.find("header", {"class": "wind-speed"})
    return val.text


def append_hdf5(group, dataset, obj):
    data = np.array([obj], dtype="i")
    if dataset not in group:
        group.create_dataset(dataset, data=data, maxshape=(None,), chunks=True)
    else:
        group[dataset].resize((group[dataset].shape[0] + len(data),))
        group[dataset][-len(data) :] = data


"""
website = "https://openweathermap.org/city/2953435"
page = requests.get(website).content
soup = bs(page, "html.parser")
# print(soup)
print(soup.find("span"))
"""
file = h5py.File("weather.hdf5", "a")
websites = pd.read_csv("websites.csv")
today = datetime.now().strftime("%y-%m-%d")
urls = [websites["URL"][i] for i in range(len(websites))]
pages = [requests.get(url) for url in urls]
scraped_pages = [bs(page.content, "html.parser") for page in pages]
temperature = [get_temp(scraped_page) for scraped_page in scraped_pages]
humidity = [get_humidity(scraped_page) for scraped_page in scraped_pages]
temperature = [to_num(temp) for temp in temperature]
humidity = [to_num(hum) for hum in humidity]
locations = websites["Location"]
# [get_loc(scraped_page) for scraped_page in scraped_pages]
wind_speeds = [get_wind_speed(scraped_page) for scraped_page in scraped_pages]
frames = {}
for i in range(len(locations)):
    frames[locations[i]] = pd.DataFrame(
        {
            "time": [today],
            "temperature": [temperature[i]],
            "humidity": [humidity[i]],
            "wind_speed": [wind_speeds[i]],
        }
    )

for frame in frames.keys():
    frames[frame].to_hdf("weather3.hdf5", key=frame)
