from dash import Dash, dcc, html, Input, Output, callback

import plotly.express as px
import plotly.graph_objects as go

# AnimalDB is a class for working with the animals.sqlite
from src.animal_db import AnimalDB

def run_app() -> None:
    app = Dash(__name__)
    app.title = 'Hello Once Again!'
    create_layout(app)
    app.run(debug=True)
    return None

def create_layout(app: Dash) -> None:
    children = []

    header = html.H1('The Best Dashboard Ever!')
    children += [header, html.Hr()]

    # First dropdown menu, select category
    cat_label = html.Label('Select a category:')
    cat_dd = dcc.Dropdown(id='cat-dd',
                          options= [''] + AnimalDB().get_category_list(),
                          value=''
                          )
    children += [cat_label, cat_dd]

    # Second dropdown menu
    subcat_label = html.Label('Select a subcategory:', 
                              id='subcat-label'
                              )
    subcat_dd = dcc.Dropdown(id='subcat-dd',
                             options=[],
                             value=''
                             )
    children += [subcat_label, subcat_dd]

    # Third dropdown menu
    item_label = html.Label('Select an animal:',
                            id='item-label'
                            )
    item_dd = dcc.Dropdown(id='item-dd',
                           options=[],
                           value=''
                           )
    children += [item_label, item_dd]

    figure_title = html.H2(id='figure-title')
    children += [figure_title]

    df = AnimalDB().get_data()
    fig = px.scatter(df, x='x', y='y')
    figure = dcc.Graph(figure=fig, id='my-figure')
    children += [figure]
    

    app.layout = html.Div(id='main-div', children=children)
    return None

@callback(
        Output('subcat-dd', 'options'),
        Output('subcat-dd', 'style'),
        Output('subcat-label', 'style'),
        Input('cat-dd', 'value')
)
def update_subcats(category: str) -> tuple[list, dict, dict]:
    vals = AnimalDB().get_subcategory_list(category)

    if len(vals):
        style = {'display': 'block'}
    else:
        style = {'display': 'none'}
    return ['']+vals, style, style

@callback(
        Output('item-dd', 'options'),
        Output('item-dd', 'style'),
        Output('item-label', 'style'),
        Input('cat-dd', 'value'),
        Input('subcat-dd', 'value')
)
def update_items(category: str, subcategory: str):
    vals = AnimalDB().get_item_list(category, subcategory)
    if len(vals):
        style = {'display': 'block'}
    else:
        style = {'display': 'none'}
    
    return ['']+vals, style, style

@callback(
        Output('my-figure', 'figure'),
        Output('figure-title', 'children'),
        Input('cat-dd', 'value'),
        Input('subcat-dd', 'value'),
        Input('item-dd', 'value')
)
def update_figure(category: str, 
                  subcategory: str, 
                  animal: str) -> tuple[go.Figure, str]:
    df = AnimalDB().get_data(category, subcategory, animal)
    fig = px.scatter(df, x='x', y='y')
    
    fig_title = ''
    if len(category):
        fig_title += f'Data for {category}'
    if len(subcategory):
        fig_title += f':{subcategory}'
    if len(animal):
        fig_title += f':{animal}'

    return fig, fig_title