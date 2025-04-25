from src.region_code import get_counties_list
from dash import Dash, dcc, html, Input, Output, callback
from ebird.api import get_observations, get_nearby_observations, get_notable_observations, get_nearby_notable, get_species_observations, get_nearby_species, get_nearest_species

import plotly.express as px
import plotly.graph_objects as go

from src.helpers import STATES
from src.helpers import COUNTY_DATA

def run_app() -> None:
    app = Dash(__name__)
    app.title = 'Bird of the Day'
    create_layout(app)
    app.run(debug = True)

    return None

def create_layout(app:Dash) -> None:
    children = []

    header = html.H1('Your bird of the day:')
    children += [header, html.Hr()]

    # First dropdown menu, select state
    state_label = html.Label('Select a state:', id = 'state-label')
    state_dd = dcc.Dropdown(id='state-dd',
                            options = [''] + STATES,
                            value = ''
                           )
    children += [state_label, state_dd]

    # Second dropdown menu, select county
    county_label = html.Label('Select a county:', id = 'county-label')
    county_dd = dcc.Dropdown(id='county-dd',
                             options = [],
                             value = ''
                            )
    children += [county_label, county_dd]

    app.layout = html.Div(id='main-div', children=children)

@callback(
    Output('county-dd', 'options'),
    Output('county-dd', 'style'),
    Output('county-label', 'style'),
    Input('state-dd', 'value')
)
def update_county(state: str) -> tuple[list, dict, dict]:
    vals = get_counties_list(state)

    if len(vals):
        style = {'display': 'block'}
    else:
        style = {'display': 'none'}
    return ['']+vals, style, style