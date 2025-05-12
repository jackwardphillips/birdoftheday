from dash import Dash, dcc, html, Input, Output, dash_table, callback
import pandas as pd
import wikipedia
import plotly.express as px
import plotly.graph_objects as go

from src.helpers import STATES, COUNTY_DATA, API_KEY
from src.bird_otd import get_nearby_list, get_species_code, get_nearby_locations, get_botd, get_graph_observations, get_common_observations, get_rare_observations, get_images, get_blurb

NEARBY_PATH = 'data/nearby_list.csv'

def run_app() -> None:
    """Launches the app."""
    app = Dash(__name__)
    app.title = 'Bird of the Day'
    create_layout(app)
    app.run(debug=False)

def create_layout(app: Dash) -> None:
    """Constructs the layout of the app."""
    children = []

    # API key storage
    stored_key = dcc.Store(id='stored-api-key', data=API_KEY)
    children += [stored_key]

    # Header
    header = html.H1('Your Bird of the Day:', style={
        'textAlign': 'center',
        'color': 'white',
        'backgroundColor': '#2F6A3A',
        'padding': '10px',
        'borderRadius': '5px'})
    children += [header]

    # Dropdowns for state, county, and bird selection
    state_label = html.Label('Select a state:')
    state_dd = dcc.Dropdown(id='state-dd', options=[''] + STATES, value='')

    county_label = html.Label('Select a county:', id='county-label')
    county_dd = dcc.Dropdown(id='county-dd', value='', options=[])

    bird_label = html.Label('Select a bird:', id='bird-label')
    bird_dd = dcc.Dropdown(id='bird-dd', value='', options=[])

    children += [state_label, state_dd, county_label, county_dd, bird_label, bird_dd]

    # Generate Bird of the Day button
    botd_button = html.Button('Generate Bird of the Day', id='botd-button', n_clicks=0,
                              style={'width': '100%', 'padding': '12px', 'backgroundColor': '#2F6A3A',
                                     'border': 'none', 'color': 'white', 'fontFamily': 'Times New Roman', 'fontSize': '16px', 'marginTop': '20px'})
    children += [botd_button, html.Hr()]

    # eBird link and nearby locations section
    ebird_link = html.Div(id='ebird-link', children=[])

    nearby_locations = html.Div([
        html.Div([
            html.Div(id='blurb', style={'marginBottom': '10px'}),
            html.Div(id='nearby-locations')
        ], style={'flex': '1', 'marginRight': '20px'}),
        html.Div(dcc.Graph(id='species-graph'), style={'flex': '1'})
    ], style={'display': 'flex', 'flexDirection': 'row', 'marginTop': '20px', 'alignItems': 'flex-start'})

    children += [ebird_link, nearby_locations, html.Hr()]

    # Common and rare sightings tables
    tables_section = html.Div([
        html.Div([html.Div(id='nearby-table', style={'marginTop': '10px'})], style={'flex': '1', 'marginRight': '20px'}),
        html.Div([html.Div(id='rare-table', style={'marginTop': '10px'})], style={'flex': '1'})
    ], style={'display': 'flex', 'marginTop': '30px', 'alignItems': 'flex-start'})

    children += [tables_section, html.Hr()]

    # Bird image slideshow
    slideshow = html.Div([
        html.Img(id='slideshow-image', style={'width': '50%', 'height': 'auto'}),
        dcc.Interval(id='image-interval', interval=5000, n_intervals=0)
    ], style={'textAlign': 'center', 'marginTop': '20px'})

    children += [slideshow]

    # Store for bird of the day
    botd_store = dcc.Store(id='botd-store')
    children += [botd_store]

    # API key status
    api_status = html.Div(id='api-key-status', style={
        'marginBottom': '1rem',
        'fontStyle': 'italic',
        'textAlign': 'center',
        'color': 'gray'
    }
)
    children += [api_status]

    app.layout = html.Div(id='main-div', children=children, style={'width': '80%', 'margin': '0 auto'})


@callback(
    Output('county-dd', 'options'),
    Output('county-dd', 'style'),
    Output('county-label', 'style'),
    Input('state-dd', 'value'),
    prevent_initial_call=False
)
def update_county(state: str) -> tuple[list, dict, dict]:
    if state:
        filtered_counties = COUNTY_DATA[COUNTY_DATA['state_name'] == state]
        vals = [{'label': county, 'value': county} for county in filtered_counties['county']]
        style = {'display': 'block'} if vals else {'display': 'none'}
    else:
        vals = []
        style = {'display': 'none'}
    return vals, style, style

@callback(
    Output('bird-dd', 'options'),
    Output('bird-dd', 'style'),
    Output('bird-label', 'style'),
    Input('state-dd', 'value'),
    Input('county-dd', 'value')
)
def update_nearby_list(state: str, county: str):
    if state and county:
        bird_list = get_nearby_list(state, county)
    else:
        bird_list = pd.DataFrame(columns=['comName', 'speciesCode'])

    vals = [{'label': bird, 'value': bird} for bird in bird_list['comName']]
    style = {'display': 'block'} if vals else {'display': 'none'}
    return vals, style, style

@callback(
    Output('ebird-link', 'children'),
    Output('nearby-locations', 'children'),
    Input('bird-dd', 'value'),
    Input('state-dd', 'value'),
    Input('county-dd', 'value')
)
def update_ebird_link(bird: str, state:str, county:str) -> tuple:
    if bird:
        species_code = get_species_code(bird)
        ebird_url = f"https://ebird.org/species/{species_code}"

        # Get 3 nearby locations
        loc1, loc2, loc3 = get_nearby_locations(bird, state, county)

        nearby_children = [
            html.H3('Recent public sightings nearby:', style={'marginTop': '20px'}),
            html.Ul([
                html.Li(loc1) if loc1 else html.Li("No location available"),
                html.Li(loc2) if loc2 else html.Li("No location available"),
                html.Li(loc3) if loc3 else html.Li("No location available"),
            ])
        ]

        return [
            html.A("Go to eBird", href=ebird_url, target="_blank", style={'fontSize': '24px', 'color': 'blue', 'textAlign': 'center'})], nearby_children
    else:
        return [], []

@callback(
    Output('botd-store', 'data'),
    Input('botd-button', 'n_clicks'),
    Input('state-dd', 'value'),
    Input('county-dd', 'value')
)
def load_botd(n_clicks, state, county):
    if n_clicks > 0 and state and county:
        botd = get_botd(state, county)
        return botd.to_dict('records')
    else:
        return []

@callback(
    Output('bird-dd', 'value'),
    Input('botd-store', 'data')
)
def init_botd(botd_data):
    return botd_data[0].get('comName', '') if botd_data else ''

@callback(
    Output('species-graph', 'figure'),
    Input('bird-dd', 'value'),
    Input('state-dd', 'value'),
    Input('county-dd', 'value'),
    prevent_initial_call=True
)
def update_species_graph(bird, state, county):
    if bird and state and county:
        df = get_graph_observations(bird, state, county)
        fig = px.bar(df, x=df.index.strftime('%Y-%m-%d'), y='Sightings',
                     labels={'x': 'Week Starting', 'Sightings': 'Number of Sightings'},
                     title=f'Sightings of {bird} in Last 4 Weeks')
        fig.update_layout(margin=dict(l=20, r=20, t=25, b=0))
        fig.update_layout(title_x=0.5)
        fig.update_layout(
            title={
            'text': f'{bird} Sightings in the Last 4 Weeks',
            'font': dict(family="Times New Roman, sans-serif", size=18, color="black", weight='bold')},
            font=dict(family="Times New Roman, sans-serif", size=12, color="black"))
        fig.update_layout(width=600, height=400)
        fig.update_xaxes(showgrid=True)
        fig.update_yaxes(showgrid=True)

        return fig
    else:
        return go.Figure()

@callback(
    Output('nearby-table', 'children'),
    Input('state-dd', 'value'),
    Input('county-dd', 'value'),
)
def update_nearby_table(state, county):
    df = get_common_observations(state, county)

    return html.H3('Most Common Sightings:', style={'marginTop': '0'}), dash_table.DataTable(
        columns=[
            {"name": "Species", "id": "comName"},
            {"name": "Total Sightings", "id": "howMany"}
        ],
        data=df.to_dict('records'),
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left', 'fontFamily': 'Times New Roman'},
        style_header={'fontWeight': 'bold', 'backgroundColor': 'white'},
        style_data={'backgroundColor': 'white'}
    )

@callback(
    Output('rare-table', 'children'),
    Input('state-dd', 'value'),
    Input('county-dd', 'value'),
)
def update_rare_species_table(state, county):
    df = get_rare_observations(state, county)
    if df.empty:
        return html.Div("No rare sightings recently.")

    return html.H3('Recent Rare Sightings:', style={'marginTop': '0'}), dash_table.DataTable(
        columns=[
            {"name": "Species", "id": "comName"},
            {"name": "Total Sightings", "id": "howMany"}
        ],
        data=df.to_dict('records'),
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left', 'fontFamily': 'Times New Roman'},
        style_header={'fontWeight': 'bold', 'backgroundColor': 'white'},
        style_data={'backgroundColor': 'white'}
    )

@callback(
    Output('slideshow-image', 'src'),
    Input('bird-dd', 'value'),
    Input('image-interval', 'n_intervals'),
)
def update_image(bird, n_intervals):
    if bird:
        if n_intervals is None:
            n_intervals = 0
        image_list = get_images(bird)
        image_index = n_intervals % len(image_list)
        return image_list[image_index]

@callback(
    Output('blurb', 'children'),
    Input('bird-dd', 'value'),
)  
def update_blurb(bird):
    if bird:
        blurb = get_blurb(bird)
        url = wikipedia.page(bird, auto_suggest=False).url
        return blurb, " (Source: ", html.A("Wikipedia", href=url, target="_blank"), ")"
    
@callback(
    Output('api-key-status', 'children'),
    Input('stored-api-key', 'data')
)
def get_api_data(API_KEY):
    if API_KEY:
        return f"You are using the dashboard with an eBird API key. Your API key is {API_KEY}."
    else:
        return "You are using the dashboard without an eBird API key. Some features may be limited and information may be out of date."