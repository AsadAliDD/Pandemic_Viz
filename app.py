import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from pprint import pprint 
from dash.dependencies import Input, Output


pandemics={'Ebola': 'ebola'}



app = dash.Dash(__name__)
app.layout = html.Div(
    [
        html.Div([
        html.H2('Pandemics Viz',
                style={'float': 'left',
                       }),
        ]),
    dcc.Dropdown(id='pandemic',
                 options=[{'label': s, 'value': s}
                          for s in pandemics.keys()],
                 value=['Ebola'],
                 multi=True
                 )
    ]
)