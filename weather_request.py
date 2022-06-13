import numpy as np
import datetime
from datetime import timezone
import requests
import time
import json
import geopy
from geopy.geocoders import Nominatim
import pandas as pd


# open weather api key
with open("api_key.txt","r") as key:
    key = key.read()

url = "https://api.openweathermap.org/data/2.5/weather?q={cityname}\&appid={APIkey}&units=metric".format(cityname="Kumasi", APIkey=key)

output = requests.get(url)

data = output.json()


# Initialize Nominatim AP
def get_geocodes(place)-> geopy.location.Location:
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
                apikey: str = key) -> json:

    """get data for an entire day"""
    url = "https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={_lat_}&lon={_long_}&units={_unit_}&dt={_stamp_}&appid={_apikey_}".format(_lat_=lat, _long_=lon, _unit_=unit, _stamp_=int(stamp), _apikey_= str(apikey))

    output = requests.get(url)
    return output,output.json()


def decode_Unix(timestamp)->str:
    """convert timestands back to understandable time formats
    Arg:
        timestamp: datetime timestamp"""
    timestamp = datetime.datetime.fromtimestamp(timestamp)
    return timestamp.strftime('%Y-%m-%d %H:%M:%S')


def json_to_pandas(jsonfile: dict, dropna: bool = True) -> pd.DataFrame:
    """Extract Relevant Data from Json File and convert to Pandas DataFrame

    json:dict|json --> Input format json file format; the output after making a Request
    dropna:bool    --> A boolean any[True,False] - removes all NaN's from the dataframe ; this will remove wind_gust and rain column

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
    for city in ("Accra","Kumasi"):
        for i in range(17-5,17):
            ctime = datetime.datetime.now()
            stamp = get_timestamp(y=ctime.year, m=ctime.month, d=ctime.day)
            print("Decoded Stamp: ", decode_Unix(stamp))
            location = get_geocodes(city)
            output = make_request(location.longitude, location.latitude, stamp)
            print(output)
            temp_data = json_to_pandas(output)
            if i==12 and city=="Accra":
                df = temp_data
            else:
                df = pd.concat((temp_data,df))
            print(stamp)

