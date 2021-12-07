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
from accounts.models import UserData

app = DjangoDash('RatingsApp')

figure = px.line()


app.layout = html.Div(children=[
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
    html.P(
        id='err',
        style={'color': 'red'}
    ),
    dcc.Graph(
        id='ratings-chart',
    )
])


@app.callback(
    Output('ratings-chart', 'figure'),
    Output('err', 'children'),
    Input('platform', 'value'),
)
def display_ratings_chart(platform, *args, **kwargs):
    abc = UserData.objects.get(id=kwargs['user'].id)
    cf_username = abc.codeforces_handle
    cc_username = abc.codechef_handle
    at_username = abc.atcoder_handle
    if platform == 'codeforces':
        ratings_data = req.get('https://codeforces.com/api/user.rating?handle=' + cf_username).json()
        name = list()
        times = list()
        ratings = list()
        for i in range(len(ratings_data['result'])):
            times.append(datetime.datetime.fromtimestamp(ratings_data['result'][i]['ratingUpdateTimeSeconds']).strftime(
                '%Y-%m-%d %H:%M:%S'))
            ratings.append(ratings_data['result'][i]['newRating'])
            name.append(ratings_data['result'][i]['contestName'])

        fig = px.line(x=times, y=ratings, hover_name=name, )
        fig.update_layout(
            xaxis_title="Date and Time",
            yaxis_title="Rating",
        )

        return fig, ''
    elif platform == 'codechef':
        if len(cc_username):
            if req.get('https://www.codechef.com/users/' + cc_username).status_code != req.codes.ok:
                return dash.no_update, 'Please enter a valid username...'
            else:
                r = req.get('https://www.codechef.com/users/' + cc_username)
                soup = BeautifulSoup(r.text, 'html.parser')
                raw_text = str(soup.find_all('script', type='text/javascript', text=re.compile('all_rating')))
                m = re.compile('all_rating').search(raw_text)
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
                names = list()

                for i in range(len(contest)):
                    x.append(contest[i]['"end_date"'][1:len(contest[i]['"end_date"']) - 1])
                    y.append(int(contest[i]['"rating"'][1:len(contest[i]['"rating"']) - 1]))
                    names.append(contest[i]['"name"'][1: len(contest[i]['"name"']) - 1])

            fig = px.line(x=x, y=y, hover_name=names)
            fig.update_layout(
                xaxis_title="Date and Time",
                yaxis_title="Rating",
            )

            return fig, ''
        else:
            return figure, 'Please enter a valid username...'
    elif platform == 'atcoder':
        if len(at_username):
            if req.get('https://atcoder.jp/users/' + at_username).status_code != req.codes.ok:
                return dash.no_update, 'Please enter a valid username...'
            else:
                r = req.get('https://atcoder.jp/users/' + at_username)
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
                name = list()

                for i in range(len(contest)):
                    x.append(datetime.datetime.fromtimestamp(int(contest[i]['"EndTime"'])).strftime('%Y-%m-%d %H:%M:%S'))
                    y.append(int(contest[i]['"NewRating"']))
                    name.append(contest[i]['"ContestName"'][1:len(contest[i]['"ContestName"']) - 1])

            fig = px.line(x=x, y=y, hover_name=name)
            fig.update_layout(
                xaxis_title="Date and Time",
                yaxis_title="Rating",
            )
            return fig, ''
        else:
            return figure, 'Please enter a valid username...'
    else:
        return figure, 'No platform selected'
