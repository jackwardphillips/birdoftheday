# Use State when you need the values from something for a callback
# but you don't want to trigger the callback when they change.
from dash import Dash, dcc, html, Input, Output, State, callback

from src.plots import plotly_line, go
from src.analysis import sigmoid

def run_app() -> None:
    app = Dash(__name__)
    app.title = 'Hello Again!'
    create_layout(app)
    app.run(debug=True)
    return None

def create_layout(app: Dash) -> None:
    children = []

    children += [html.H1('Sigmoids are great!'), html.Hr()]
    label_a = dcc.Markdown(id='label-a',
                           mathjax=True,
                           style={'font-size': '20px'}
                           )
    slider_a = dcc.Slider(id='sig-a',
                         min=0,
                         max=10,
                         step=0.01,
                         value=1,
                         marks=None,
                         tooltip={'template': '{value}'}
                         )
    children += [label_a, slider_a]

    label_k = dcc.Markdown(id='label-k',
                           mathjax=True,
                           style={'font-size': '20px'}
                           )
    slider_k = dcc.Slider(id='sig-k',
                         min=0,
                         max=10,
                         step=0.01,
                         value=1,
                         marks=None,
                         tooltip={'template': '{value}'}
                         )
    children += [label_k, slider_k]

    equation = dcc.Markdown(id='sig-equation',
                            mathjax=True,
                            style={'text-align': 'center',
                                   'font-size': '32px'}
                            )
    figure = dcc.Graph(id='fig-sigmoid',
                       figure=update_figure(a=1, k=1)
                       )
    children += [equation, figure]

    download_button = html.Button('Download Figure',
                                  id='download-figure-button',
                                  n_clicks=0
                                  )
    download = dcc.Download(id='download-figure-object')
    children += [download_button, download]

    app.layout = html.Div(id='main-div', children=children,
                          style={'max-width': '640px'}
                          )
    return None

@callback(
        Output(component_id='fig-sigmoid', component_property='figure'),
        Input(component_id='sig-a', component_property='value'),
        Input(component_id='sig-k', component_property='value')
)
def update_figure(a: float, k: float) -> go.Figure:
    x, y = sigmoid(a, k)
    fig = plotly_line(x, y)
    return fig
@callback(
        Output(component_id='sig-equation', component_property='children'),
        Output(component_id='label-a', component_property='children'),
        Output(component_id='label-k', component_property='children'),
        Input(component_id='sig-a', component_property='value'),
        Input(component_id='sig-k', component_property='value')
)
def update_equation_and_labels(a: float, 
                               k: float
                               ) -> tuple[str, str, str]:
    label_a = rf"$a={a}$"
    label_k = rf"$k={k}$"
    eq = rf"$y=\frac{{1}}{{1+\left(\frac{{1}}{{x^{{{a}}}}}-1\right)^{{{k}}}}}$"
    return eq, label_a, label_k

@callback(
        Output(component_id='download-figure-object', component_property='data'),
        Input(component_id='download-figure-button', component_property='n_clicks'),
        State(component_id='sig-a', component_property='value'),
        State(component_id='sig-k', component_property='value'),
        prevent_initial_call=True
)
def download_figure(_, a: float, k: float) -> dict:
    filename = f"sigmoid_a={a}_k={k}.html"
    return dict(content=update_figure(a, k).to_html(), 
                filename=filename)