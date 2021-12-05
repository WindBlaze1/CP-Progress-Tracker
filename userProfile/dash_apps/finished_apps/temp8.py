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

app = DjangoDash("Updater")

app.layout = html.Div([
    html.Br(),
    html.Br(),
    html.Label(
        children='Codechef handle: ',
        id='codechef_updated_handle',
    ),
    dcc.Input(
        id='cc_handle',
        value='',
        placeholder='updated Codechef handle',
    ),
    html.Br(),
    html.Br(),
    html.Label(
        children='Atcoder handle: ',
        id='atcoder_updated_handle',
    ),
    dcc.Input(
        id='at_handle',
        value='',
        placeholder='updated Atcoder handle',
    ),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Div(id='button_div', style={'text-align-last': 'center'}, children=html.Button(
        id='submit',
        n_clicks=0,
        children='Submit',
        style={
            'display': 'inline-block',
            'background-color': '#214a80',
            'border-radius': '10px',
            'border': '4px double #cccccc',
            'text-align': 'center',
            'transition': 'all 0.5s',
            'cursor': 'pointer',
            'color': '#ffffff'
        }
    ),),
    html.Br(),
    html.Div(
        id='outputs',
        style={
            'color': 'red'
        }
    )
])


def codechef_check(username):
    r = req.get('https://www.codechef.com/users/' + username)
    soup = BeautifulSoup(r.text, 'html.parser')
    page_title = str(soup.find_all('title')[0])
    if username in page_title:
        return True
    else:
        return False


def atcoder_check(username):
    r = req.get('https://atcoder.jp/users/' + username)
    soup = BeautifulSoup(r.text, 'html.parser')
    page_title = str(soup.find_all('title')[0])
    if username in page_title:
        return True
    else:
        return False


@app.callback(
    Output('outputs', 'children'),
    Input('submit', 'n_clicks'),
    State('cc_handle', 'value'),
    State('at_handle', 'value'),
)
def updating(n_cl, cc, at, **kwargs):
    abc = UserData.objects.get(id=kwargs['user'].id)
    code, atc = False, False
    if len(cc):
        if codechef_check(cc):
            abc.codechef_handle = cc
            abc.save()
        else:
            code = True

    if len(at):
        if atcoder_check(at):
            abc.atcoder_handle = at
            abc.save()
        else:
            atc = True

    if len(cc) and len(at):
        if (not code) and (not atc):
            return 'Codechef and Atcoder username updated successfully'
        elif not code:
            return 'Codechef username updated successfully\nAtcoder username was wrong'
        elif not atc:
            return 'Atcoder username updated successfully\nCodechef username was wrong'
        else:
            return 'Both Codechef and Atcoder usernames are wrong'
    elif len(cc):
        if (not code):
            return 'Codechef username updated successfully'
        else:
            return 'Wrong Codechef username'
    elif len(at):
        if not atc:
            return 'Atcoder username updated successfully'
        else:
            return 'Wrong Atcoder username'
    else:
        return ''
