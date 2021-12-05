from django_plotly_dash import DjangoDash
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.graph_objects as go
from bs4 import BeautifulSoup
import pandas as pd
import re
import requests as req
import datetime
from accounts.models import UserData

app = DjangoDash("AcceptanceChart")

fig = go.Figure(data=[go.Pie()])

app.layout = html.Div([
    dcc.Graph(
        id='ac_chart',
        style={
            'width': '100%',
            'height': '230px',
        }
    ),
    dcc.Textarea(
        id='nothing',
        hidden=1
    )
])


@app.callback(
    Output('ac_chart', 'figure'),
    Input('nothing', 'value')
)
def display_ratings_chart(vals, *args, **kwargs):
    abc = UserData.objects.get(id=kwargs['user'].id)
    return px.pie(names=['Accepted', 'Wrong Answer'], values=[abc.num_ques_solved, abc.num_ques_att - abc.num_ques_solved])


