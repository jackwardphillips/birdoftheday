import json
import requests
import pandas as pd
import geopy

# courtesy of https://simplemaps.com/data/us-counties
from src.helpers import COUNTY_DATA, LOADED_REGION_CODES

def get_region_code(county: str, state: str, coords: bool = False) -> str:
    """
    Fetches the region code for a given county and state based on latitude and longitude.

    This function first checks if the region code for the given county and state is already 
    loaded from a cached dataset. If it is not found, it makes a request to a publicly available
    API to fetch the region code using the county's latitude and longitude.

    Parameters:
        county (str): The name of the county.
        state (str): The name of the state.
        coords (bool): A flag indicating if latitude and longitude should be returned alongside 
                       the region code. Defaults to False.

    Returns:
        str: The region code for the given county and state.
        tuple (str, float, float): If `coords=True`, returns the region code along with latitude and longitude.
    """
    global LOADED_REGION_CODES
    
    # GET LAT AND LNG
    lat = COUNTY_DATA.loc[(COUNTY_DATA['county'] == county) & (COUNTY_DATA['state_id'] == state), 'lat'].iloc[0]
    lng = COUNTY_DATA.loc[(COUNTY_DATA['county'] == county) & (COUNTY_DATA['state_id'] == state), 'lng'].iloc[0]

    # GET REGION CODE
    if lat in LOADED_REGION_CODES['lat'].to_list() and lng in LOADED_REGION_CODES['lng'].to_list():
        region_code = LOADED_REGION_CODES[
            (LOADED_REGION_CODES['lat'] == lat) & (LOADED_REGION_CODES['lng'] == lng)
        ]['region_code'].values[0]

    else:
        # this municipal API is a publicly available, no keys needed
        census_url = f'https://geo.fcc.gov/api/census/area?lat={lat}&lon={lng}&format=json'
    
        # send out a GET request
        payload = {}
        get = requests.request("GET", census_url, params=payload)
    
        # parse the response, all API values are contained in list 'results'
        response = json.loads(get.content)['results'][0]
    
        # use the last three digits from the in-state FIPS code as the "subnational 2" identifier
        fips = response['county_fips']
    
        # assemble and return the "subnational type 2" code
        region_code = f'US-{response["state_code"]}-{fips[2]}{fips[3]}{fips[4]}'
        print(f'formed region code: {region_code}')

        # save region code
        new_entry = {'county': county, 'state': state, 'region_code': region_code, 'lat': lat, 'lng': lng}
        LOADED_REGION_CODES = pd.concat([LOADED_REGION_CODES, pd.DataFrame([new_entry])], ignore_index=True)
        LOADED_REGION_CODES.to_csv('data/loaded_region_codes.csv', index=False)
    
    if coords:
        return region_code, lat, lng
    else:
        return region_code

def get_counties_list(state: str) -> list:
    """
    Retrieves a list of counties for a given state.

    Parameters:
        state (str): The name of the state.

    Returns:
        list: A list of county names for the given state.
    """
    county_list = COUNTY_DATA[COUNTY_DATA['state_name'] == state]['county'].tolist()
    return county_list
