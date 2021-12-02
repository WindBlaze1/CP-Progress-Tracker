from django_plotly_dash import DjangoDash
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.express as px
from bs4 import BeautifulSoup
import pandas as pd
import re
import requests as req
import datetime

app = DjangoDash('RatingsApp')

figure = px.line(x=[i for i in range(0, 1001, 100)], y=[i for i in range(0, 1001, 100)])

# app.layout = html.Div([
#     dcc.Graph(id='some', figure=figure)
# ])

app.layout = html.Div([
    dcc.Dropdown(
        options=[
            {'label': 'Codeforces', 'value': 'codeforces'},
            {'label': 'Codechef', 'value': 'codechef'},
            {'label': 'Atcoder', 'value': 'atcoder'}
        ],
        value='codeforces',
        id='platform',
    ),
    html.Br(),
    dcc.Input(
        id='username',
        type='text',
        placeholder='Your handle',
        value=''
    ),
    html.Br(),
    html.Button(
        id='submit-button',
        n_clicks=0,
        children='Submit'
    ),
    html.Br(),
    html.P(
        id='err',
        style={'color': 'red'}
    ),
    dcc.Graph(
        id='ratings-chart',
    )
])


@app.callback(
    Output('handle', 'children'),
    Input('platform', 'value')
)
def handle_name(value):
    if value == 'codeforces':
        return 'Enter Codeforces handle: '
    elif value == 'codechef':
        return 'Enter Codechef handle: '
    elif value == 'atcoder':
        return 'Enter Atcoder handle: '
    else:
        return 'Enter handle: '


@app.callback(
    Output('ratings-chart', 'figure'),
    Output('err', 'children'),
    Input('submit-button', 'n_clicks'),
    State('username', 'value'),
    State('platform', 'value'),
)
def display_ratings_chart(n_clicks, username, platform):
    if n_clicks is None or 0:
        raise PreventUpdate
    else:
        if platform == 'codeforces':
            if req.get('https://codeforces.com/api/user.info?handles=' + username).json()['status'] == 'FAILED':
                return dash.no_update, 'Please enter a valid username...'
            else:
                # user_details = req.get('https://codeforces.com/api/user.info?handles=' + username).json()
                ratings_data = req.get('https://codeforces.com/api/user.rating?handle=' + username).json()
                # print(ratings_data)
                times = []
                ratings = []
                for i in range(len(ratings_data['result'])):
                    times.append(datetime.datetime.fromtimestamp(ratings_data['result'][i]['ratingUpdateTimeSeconds']).strftime(
                        '%Y-%m-%d %H:%M:%S'))
                    ratings.append(ratings_data['result'][i]['newRating'])
                return px.line(x=times, y=ratings), ''
        elif platform == 'codechef':
            if req.get('https://www.codechef.com/users/' + username).status_code != req.codes.ok:
                return dash.no_update, 'Please enter a valid username...'
            else:
                r = req.get('https://www.codechef.com/users/sparsh_1234')
                soup = BeautifulSoup(r.text, 'html.parser')
                raw_text = str(soup.find_all('script', type='text/javascript', text=re.compile('all_rating')))
                print(re.compile('all_rating').search(raw_text))
                m = re.compile('all_rating').search(raw_text)
                print(m.start(), m.end())
                i = m.end() + 3
                m = raw_text
                # print(m)
                contest = list()
                while m[i] != ']':
                    if m[i] == '{':
                        i += 1
                        sample = dict()
                        while m[i] != ']' and m[i] != '}':
                            ans1 = str()
                            ans2 = str()
                            while m[i] != ']' and m[i] != ':':
                                ans1 += m[i]
                                i += 1
                            i += 1
                            flag = True
                            while m[i] != ']' and m[i] != ',':
                                if m[i] == '}':
                                    flag = False
                                    break
                                ans2 += m[i]
                                i += 1
                            sample[ans1] = ans2
                            if flag:
                                i += 1
                        contest.append(sample)
                    else:
                        i += 1

                x = list()
                y = list()

                for i in range(len(contest)):
                    x.append(contest[i]['"end_date"'][1:len(contest[i]['"end_date"']) - 1])
                    y.append(int(contest[i]['"rating"'][1:len(contest[i]['"rating"']) - 1]))
            return px.line(x=x, y=y), ''
        elif platform == 'atcoder':
            if req.get('https://atcoder.jp/users/' + username).status_code != req.codes.ok:
                return dash.no_update, 'Please enter a valid username...'
            else:
                r = req.get('https://atcoder.jp/users/' + username)
                soup = BeautifulSoup(r.text, 'html.parser')
                participated_contests = str(soup.find_all('script', text=re.compile('rating_history')))
                participated_contests = participated_contests[28:len(participated_contests) - 11]
                contest = list()
                i = 0
                while i != len(participated_contests):
                    if participated_contests[i] == '{':
                        i += 1
                        sample = dict()
                        while i != len(participated_contests) and participated_contests[i] != '}':
                            ans1 = str()
                            ans2 = str()
                            while i != len(participated_contests) and participated_contests[i] != ':':
                                ans1 += participated_contests[i]
                                i += 1
                            i += 1
                            flag = True
                            while i != len(participated_contests) and participated_contests[i] != ',':
                                if participated_contests[i] == '}':
                                    flag = False
                                    break
                                ans2 += participated_contests[i]
                                i += 1
                            sample[ans1] = ans2
                            if flag:
                                i += 1
                        contest.append(sample)
                    else:
                        i += 1
                x = list()
                y = list()
                for i in range(len(contest)):
                    x.append(datetime.datetime.fromtimestamp(int(contest[i]['"EndTime"'])).strftime('%Y-%m-%d %H:%M:%S'))
                    y.append(int(contest[i]['"NewRating"']))
            print(x)
            return px.line(x=x, y=y), ''
        else:
            return dash.no_update, dash.no_update
