import pytest
from weather_request import *
import geopy
import jsonschema
from jsonschema import validate
from datetime import datetime,timezone


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
def current_datetime():
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
    a timestamp into datetime
    
    Args:
        test_get_timestand: A fixture for testing the get_timestamp function"""

    decode_Unix(test_get_timestamp)

    


def test_make_request(test_get_geocode,test_get_timestamp):
    """A test function for the make_request function
    For this function to run, the get_geocode and get_timestamp should
    not produce  errors after test
     Args:
        test_get_geocode
        test_get_timestamp
    Return:
        data = json file containig request data from OpenWeather
        """

    try:
        latitude = test_get_geocode.latitude
        longitude = test_get_geocode.longitude
        stamp = test_get_timestamp
    except:
        raise ArgumentError("An argument of this function Failed")
    
    else:
        assert make_request(lon = longitude,lat = latitude,stamp = stamp)[0].status_code == 200


def validateJson(test_make_request):

    try:
        assert isinstance(test_make_request[1],json)
        validate(instance=jsonData, schema=test_make_request[1])
        
    except jsonschema.exceptions.ValidationError as err:
        print("Output is a Invalid")
