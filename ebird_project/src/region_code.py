import json
import requests
import pandas as pd

# courtesy of https://simplemaps.com/data/us-counties
from src.helpers import COUNTY_DATA

def get_lat_lng(county:str, state:str) -> tuple[float, float]:
    """
    """
    lat = COUNTY_DATA.loc[(COUNTY_DATA['county'] == county) & (COUNTY_DATA['state_id'] == state), 'lat'].iloc[0]
    lng = COUNTY_DATA.loc[(COUNTY_DATA['county'] == county) & (COUNTY_DATA['state_id'] == state), 'lng'].iloc[0]

    return lat, lng
    
def get_region_code(lat:float, lng:float) -> int:
    """
    
    """
    # this municipal api is a publicly available, no keys needed
    census_url = str('https://geo.fcc.gov/api/census/area?lat=' +
                     str(lat) +
                     '&lon=' +
                     str(lng) +
                     '&format=json')

    # send out a GET request:
    payload = {}
    get = requests.request("GET", census_url, data=payload)

    # parse the response, all api values are contained in list 'results':
    response = json.loads(get.content)['results'][0]

    # use the last three digits from the in-state fips code as the "subnational 2" identifier:
    fips = response['county_fips']

    # assemble and return the "subnational type 2" code:
    region_code = 'US-' + response['state_code'] + '-' + fips[2] + fips[3] + fips[4]
    print('formed region code: ' + region_code)
    return region_code

def get_counties_list(state:str) -> list:
    county_list = COUNTY_DATA[COUNTY_DATA['state_name'] == state]['county'].tolist()
    return county_list