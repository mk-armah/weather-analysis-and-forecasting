"""
Author: Eng. Michael Kofi Armah
Detail : Library for making weather requests
Date Created : 4/1/22
Last Modified : 6/18/22
"""


import numpy as np
import datetime
from datetime import timezone
import requests
import time
import json
import geopy
from geopy.geocoders import Nominatim
import pandas as pd

from dotenv import dotenv_values

credentials = dotenv_values(".env")


# Initialize Nominatim AP
def get_geocodes(place) -> geopy.location.Location:
    """
    Gets the geographic cordinates of a given location
    pass location by name, e.g A city name like 'Accra'
    Args:
        place:str, valid earth location, city or town
    
    Return:
        location, contains
    """

    geolocator = Nominatim(user_agent="MyApp")
    location = geolocator.geocode(place)

    return location


def get_timestamp(y: int, m: int, d: int)->float:
    """convert time to a Unix timestamp
    Args:

        y:int  --> Year .e.g 2022
        m:int  --> Month, Month should be an inter of range 1 to 12 inclusive e.g. 3,indicating the month March
        d:int  --> Day of the month; should be an integer
    Return:
        timestamp
    
    stamp = get_timestamp(y = 2022,m = 3,d = 30)
    print(stamp)
    >>> 1648598400.0 """

    dt = datetime.datetime(y, m, d,tzinfo=timezone.utc)
    utc_time = dt.replace(tzinfo=timezone.utc)
    utc_timestamp = utc_time.timestamp()
    return utc_timestamp


def make_request(lon:float, lat:float,
                stamp: int, unit: str = "metric",
                apikey: str = credentials["APIKEY"]) -> tuple:

    """get data for an entire day
    Args:
        lon (Longitude) | float: Longitudinal cordinate of the location under study
        lat; (Latitude) | float: Latitudinal cordinate of the location under study
        stamp (timestamp) | int: Utc Timestamp of the desired time 
        apikey (API Key) | str: Open Weather Map API access key

    Return:
        json file containing the requested weather data
        """

    url = "https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={_lat_}&lon={_long_}&units={_unit_}&dt={_stamp_}&appid={_apikey_}".format(_lat_=lat, _long_=lon, _unit_=unit, _stamp_=int(stamp), _apikey_= apikey)

    output = requests.get(url)
    return output, output.json()


def decode_Unix(timestamp)->str:
    """convert timestamps back to understandable time formats
    Arg:
        timestamp: datetime timestamp"""

    timestamp = datetime.datetime.fromtimestamp(timestamp)
    return timestamp.strftime('%Y-%m-%d %H:%M:%S')


def json_to_pandas(jsonfile: dict, dropna: bool = True) -> pd.DataFrame:
    """Extract Relevant Data from Json File and convert to Pandas DataFrame

    json:dict|json --> Input format json file format; the output after making a Request
    dropna:bool    --> A bool, any[True,False] - removes all NaN's from the dataframe if True; this will remove wind_gust and rain column

    Note : Not all columns in the Samples In the Json file have wind_gust and rain values"""

    df = pd.DataFrame(jsonfile['hourly'])  #
    df['zone'] = jsonfile['timezone'].split("/")[1]  # get city

    for i in range(len(df)):
        if i == 0:
            weather_data = pd.DataFrame(df["weather"][i])
        else:
            weather_data = pd.concat(
                (weather_data, pd.DataFrame(
                    df["weather"][i])), axis=0)

    weather_data.reset_index(inplace=True, drop=True)

    df = df.join(weather_data, how="outer")
    # returns a DataFrame free of NaN's if dropna is specified as True
    df = df.dropna(axis=1) if dropna else df
    # drop weather after extracting features
    df = df.drop(columns=['weather'], axis=1)

    return df


if __name__ == "__main__":
    print(credentials["APIKEY"])
    ctime = datetime.datetime.now()
    stamp = get_timestamp(y=ctime.year, m=ctime.month, d=ctime.day)
    print("Decoded Stamp: ", decode_Unix(stamp))
    location = get_geocodes("Accra")
    output = make_request(location.longitude, location.latitude, stamp)
    print(output[1])
    temp_data = json_to_pandas(output[1])
    print(temp_data.head(24))