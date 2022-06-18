"""
Author: Eng. Michael Kofi Armah
This is a Test Script for weather_request functions
Date Created: 6/11/22
Date Modified: 6/18/22
"""


import pytest
from weather_request import *
import geopy
import jsonschema
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from datetime import datetime, timezone
import pandas as pd



@pytest.fixture
def test_get_geocode():
    locations = [
                "Accra","Porto-Novo","Ouagadougou",
                "Praia","Banjul","Conakry","Bissau",
                "Yamoussoukro","Monrovia","Bamako",
                "Nouakchott","Niamey","Dakar",
                "Freetown","Lomé","Abuja"
                ]

    for i in locations:
        try:
            code = get_geocodes(i)
            assert isinstance(code,geopy.location.Location)

        except AssertionError:
            print("Output For {} is not Geopy Instance".format(i))

    return code


@pytest.fixture
def current_datetime() -> datetime:
    """Get the current time"""
    ctime = datetime.now(tz=timezone.utc)
    return ctime


@pytest.fixture
def test_get_timestamp(current_datetime):
    """Get timestamp"""

    try:
        #check whether get_timestamp code doesn't produce major error
        stamp =  get_timestamp(
            y = current_datetime.year,
            m = current_datetime.month,
            d = current_datetime.day,
        )
    except:
        raise RuntimeError("Major Bug in get_timestamp func needs a Fix")
    
    else:
        assert  isinstance(stamp,float)
    
    return stamp


def test_decode_Unix(test_get_timestamp):
    """Test decode_Unix function,
    the decode Unix function to be tested converts
    a timestamp into datetime with custom formats
    
    Args:
        test_get_timestand: A fixture for testing the get_timestamp function"""
    try:
        assert isinstance(decode_Unix(test_get_timestamp),str)
    
    except AssertionError as error:
        raise error("Time Stamp is not an instance of datetime")


@pytest.fixture
def request_data(test_get_geocode, test_get_timestamp):
    """make data request function using the make_request function
    For this function to run, the get_geocode and get_timestamp should
    not produce  errors after test
     Args:
        test_get_geocode
        test_get_timestamp
    Return:
        data = json file containig request data from OpenWeather
        """

    latitude = test_get_geocode.latitude
    longitude = test_get_geocode.longitude
    stamp = test_get_timestamp

    request_data = make_request(lon = longitude, lat = latitude, stamp = stamp)

    return request_data

def test_make_request(request_data):
    """A test function for the make_request function
     Args:
        request_data | pytest fixture: makes request to Open Weather using make_request function
        """

# define a schema for validating the requested json data
    schema = {
    "type": "object",
    "properties": {
        "timezone": {"type": "string"},
        "lon": {"type": "number"},
        "lat": {"type": "number"},
        "hourly": {"type": "array"}
        },
    "required": ["hourly", "timezone", "lat", "lon"],
    "dependentRequired": {"hourly": ["timezone"]}
    }
    
    try:
        assert request_data[0].status_code == 200
        assert len(request_data[1]) > 1
        validate(instance=request_data[1], schema=schema)

    except AssertionError:
        print("API DATA REQUEST FAILED")

    except ValidationError:
        print("Json Data failed Validation")


def test_json_to_pandas(request_data):
    """ Test the json_to_pandas function
    Args:
        request_data | pytest fixture: makes request to Open Weather using make_request function"""
    
    assert isinstance(json_to_pandas(jsonfile=request_data[0], dropna = True),pd.DataFrame)

