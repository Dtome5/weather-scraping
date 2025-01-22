import requests
import h5py
import pandas as pd
import re
import json
import urllib.request
import numpy as np
import openmeteo_requests
import requests_cache
from retry_requests import retry

from datetime import datetime, timedelta
from bs4 import BeautifulSoup as bs
from requests.models import LocationParseError

def to_num(var: str):
    # convert string to number
    new_val = ""
    for i in var:
        if i.isnumeric() == True:
            new_val += i
    return int(new_val)

# retrieves temperature
def get_temp(soup: bs):
    val = soup.select_one(".CurrentConditions--tempValue--zUBSz")
    return val.text

# retrieves humidity
def get_humidity(soup: bs):
    val = soup.select_one(
        "div.WeatherDetailsListItem--WeatherDetailsListItem--HLP3I:nth-child(3) > div:nth-child(3) > span:nth-child(1)"
    )
    return val.text

# retrieves location
def get_loc(soup: bs):
    val = soup.select_one(".CurrentConditions--location--yub4l")
    return val.text

# retrieves wind speed
def get_wind_speed(soup: bs):
    val = soup.select_one(".Wind--windWrapper--NsCjc > span:nth-child(2)")
    return val.text


# retrieves historical data using openmeteo API
def meteo(loc, lat, long):
    cache_session = requests_cache.CachedSession(".cache", expire_after=-1)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)
    url = "https://archive-api.open-meteo.com/v1/archive"
    end_date = datetime.now()
    start_date = end_date - timedelta(days=14)
    params = {
        "latitude": lat,
        "longitude": long,
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "hourly": ["temperature_2m", "relative_humidity_2m", "wind_speed_10m"],
        "temporal_resolution": "hourly_6",
    }

    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]

    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
    hourly_wind_speed_10m = hourly.Variables(2).ValuesAsNumpy()

    hourly_data = {
        "time": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left",
        )
    }

    hourly_data["temperature"] = hourly_temperature_2m
    hourly_data["humidity"] = hourly_relative_humidity_2m
    hourly_data["wind_speed"] = hourly_wind_speed_10m

    hourly_dataframe = pd.DataFrame(data=hourly_data)
    return hourly_dataframe


# imports webpage list from csv
websites = pd.read_csv("websites.csv")
today = datetime.now().strftime("%Y-%m-%d %H:%M")
# creates list of urls from dataframe
urls = [websites["URL"][i] for i in range(len(websites))]
# gets pages
pages = [requests.get(url) for url in urls]
# parses html
scraped_pages = [bs(page.content, "html.parser") for page in pages]
# retrieve parameters
temperature = [get_temp(scraped_page) for scraped_page in scraped_pages]
humidity = [get_humidity(scraped_page) for scraped_page in scraped_pages]
# convert to integers
temperature = [to_num(temp) for temp in temperature]
humidity = [to_num(hum) for hum in humidity]
locations = websites["Location"]
wind_speeds = [get_wind_speed(scraped_page) for scraped_page in scraped_pages]
# creates dataframes for locations
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
# saves dataframes to hdf5
for frame in frames.keys():
    with pd.HDFStore("weather.hdf5",mode="a") as hdf:
        hdf.append(frame,frames[frame])

        # frames[frame].to_hdf("weather3.hdf5",mode="a", key=frame,append=True)
# for frame in frames.keys():
#     print(pd.read_hdf("weather3.hdf5",mode="r",key = frame))
print(datetime.now())
def past():
    frames={}
    frames["London"] = meteo("London", 51.5085, -0.1257)
    frames["Bad_Honnef"] = meteo("London", 50.6434, 7.2278)
    frames["Abuja"] = meteo("London", 9.0579, 7.4951)
    for frame in frames.keys():
        with pd.HDFStore("weather.hdf5",mode="a") as hdf:
            hdf.append(frame,frames[frame])
