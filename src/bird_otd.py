import pandas as pd
import datetime as dt
import wikipedia
import os
from ebird.api import (
    get_observations,
    get_nearby_observations,
    get_notable_observations,
    get_nearby_species,
    get_species_observations,
)

from src.region_code import get_region_code
from src.helpers import LIFE_LIST, API_KEY, ABBREIVIATIONS, haversine

def get_botd(state: str = None, county: str = None) -> pd.DataFrame:
    """
    Returns the most commonly observed bird in the region that is not already in the LIFE_LIST.
    Uses cached data if API_KEY is not provided.
    """
    cache_file = 'data/botd.csv'
    if state and county:
        abbr = ABBREIVIATIONS.get(state, None)
        region_code, lat, lng = get_region_code(county, abbr, coords=True)

        if API_KEY:
            df = pd.DataFrame(get_observations(API_KEY, region_code))
            df = df.groupby('comName')['howMany'].sum().reset_index().sort_values(by='howMany', ascending=False)
            df.to_csv(cache_file, index=False)
        else:
            df = pd.read_csv(cache_file)

        bird_of_the_day = df[~df['comName'].isin(LIFE_LIST)]
        return bird_of_the_day.head(1)

def get_nearby_list(state: str = None, county: str = None) -> pd.DataFrame:
    """
    Returns a DataFrame of recent nearby bird observations.
    Uses cached data if API_KEY is not provided.
    """
    cache_file = 'data/nearby_list.csv'
    if state and county:
        abbr = ABBREIVIATIONS.get(state, None)
        _, lat, lng = get_region_code(county, abbr, coords=True)

        if API_KEY:
            nearby = pd.DataFrame(get_nearby_observations(API_KEY, lat, lng, dist=50, back=30))[['comName', 'speciesCode']]
            nearby = nearby.sort_values(by='comName').reset_index(drop=True)
            nearby.to_csv(cache_file, index=False)
        else:
            nearby = pd.read_csv(cache_file)
    else:
        nearby = pd.read_csv(cache_file)

    return nearby

def get_species_code(bird: str) -> str:
    """
    Returns the species code for a given bird based on nearby observations.
    """
    nearby = pd.read_csv('data/nearby_list.csv')
    code = nearby[nearby['comName'] == bird]['speciesCode'].values[0]
    return code

def get_nearby_locations(bird: str, state: str, county: str) -> tuple:
    """
    Returns a tuple of the three closest public locations where the specified bird
    has been recently observed.
    Uses cached data if API_KEY is not provided.
    """
    cache_file = 'data/nearby_species_locations.csv'
    code = get_species_code(bird)
    abbr = ABBREIVIATIONS.get(state, None)
    _, lat, lng = get_region_code(county, abbr, coords=True)

    if API_KEY:
        observations = get_nearby_species(API_KEY, code, lat, lng, dist=25, back=7)
        public_observations = [obs for obs in observations if not obs['locationPrivate']]

        for obs in public_observations:
            obs['distance'] = round(haversine(lat, lng, obs['lat'], obs['lng']), 2)

        public_observations.sort(key=lambda x: x['distance'])
        top_3 = public_observations[:3]

        pd.DataFrame(top_3).to_csv(cache_file, index=False)
    else:
        top_3 = pd.read_csv(cache_file).to_dict(orient='records')[:3]

    top_3_list = [None, None, None]
    for i in range(len(top_3)):
        top_3_list[i] = (top_3[i]['locName'], ', ', top_3[i]['distance'], ' km')

    return top_3_list[0], top_3_list[1], top_3_list[2]

def get_graph_observations(bird: str, state: str, county: str) -> pd.DataFrame:
    """
    Returns a DataFrame counting bird sightings over each of the past 4 weeks for a given bird.
    Uses cached data if API_KEY is not provided.
    """
    cache_file = 'data/graph_observations.csv'
    code = get_species_code(bird)
    abbr = ABBREIVIATIONS.get(state, None)
    _, lat, lng = get_region_code(county, abbr, coords=True)

    if API_KEY:
        all_obs = get_nearby_species(API_KEY, code, lat, lng, dist=25, back=28)

        week_buckets = [0, 0, 0, 0]
        now = dt.datetime.now()
        week_start_dates = [now - dt.timedelta(weeks=w) for w in range(4, 0, -1)]
        week_end_dates = [start + dt.timedelta(days=7) for start in week_start_dates]

        for obs in all_obs:
            obs_date_str = obs.get("obsDt")
            if not obs_date_str:
                continue
            try:
                obs_date = dt.datetime.strptime(obs_date_str.split(" ")[0], "%Y-%m-%d")
            except ValueError:
                continue

            for i, (start, end) in enumerate(zip(week_start_dates, week_end_dates)):
                if start <= obs_date < end:
                    week_buckets[i] += 1
                    break

        df = pd.DataFrame({'Sightings': week_buckets}, index=week_start_dates)
        df.to_csv(cache_file)
    else:
        df = pd.read_csv(cache_file, index_col=0, parse_dates=True)

    return df

def get_common_observations(state: str, county: str) -> pd.DataFrame:
    """
    Returns the 10 most commonly observed birds over the past 14 days in a given region.
    Uses cached data if API_KEY is not provided.
    """
    cache_file = 'data/common_observations.csv'
    if state and county:
        abbr = ABBREIVIATIONS.get(state, None)
        region_code = get_region_code(county, abbr, coords=False)

        if API_KEY:
            df = pd.DataFrame(get_observations(API_KEY, region_code, back=14))
            df = df.groupby('comName')['howMany'].sum().reset_index().sort_values(by='howMany', ascending=False)
            df.to_csv(cache_file, index=False)
        else:
            df = pd.read_csv(cache_file)

        return df.head(10)

def get_rare_observations(state: str, county: str) -> pd.DataFrame:
    """
    Returns a DataFrame of rare bird sightings in a given region.
    Uses cached data if API_KEY is not provided.
    """
    cache_file = 'data/rare_observations.csv'
    if state and county:
        abbr = ABBREIVIATIONS.get(state, None)
        region_code = get_region_code(county, abbr, coords=False)

        if API_KEY:
            df = pd.DataFrame(get_notable_observations(API_KEY, region_code, back=14))
            df = df.groupby('comName')['howMany'].sum().reset_index().sort_values(by='howMany', ascending=False)
            df.to_csv(cache_file, index=False)
        else:
            df = pd.read_csv(cache_file)

        return df

def get_images(bird: str) -> list:
    """
    Returns a list of .jpg image URLs of the bird from Wikipedia.
    """
    try:
        search_results = wikipedia.search(bird)
        if search_results:
            page = wikipedia.page(search_results[0], auto_suggest=False)
            jpg_images = [img for img in page.images if img.lower().endswith('.jpg')]
            return jpg_images
        return []
    except wikipedia.exceptions.WikipediaException as e:
        print(f"Error fetching image for {bird}: {str(e)}")
        return []

def get_blurb(bird: str) -> str:
    """
    Returns a short introductory summary of the bird from Wikipedia.
    """
    try:
        blurb = wikipedia.summary(bird, sentences=20, auto_suggest=False)
        blurb_intro = wikipedia.summary(bird, sentences=5, auto_suggest=False).split('=')[0]
        if 'Description' in blurb:
            blurb_intro += blurb.split('=')[4]
        return blurb_intro
    except wikipedia.exceptions.WikipediaException as e:
        print(f"Error fetching summary for {bird}: {str(e)}")
        return "Summary not available."