# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import yfinance as yf

def build_dataframe(ticker, length):
    msft = yf.Ticker(ticker)
    hist = msft.history(period=length)
    return hist.reset_index()

def format_for_bar(df):
    df['Month'] = df['Date'].apply(lambda x: x.month)
    df['Month'] = pd.Categorical(df['Month'])
    return df.groupby('Month').agg({"Volume": "mean"}).reset_index()

def build_dash(server):
    app = Dash(server = server, name='DashboardApp', url_base_pathname='/dashapp/')

    app.layout = html.Div(children=[
        html.H1(children='Quick Dash by Kireto'),

        html.Div(children='''
            Dash: A web application framework for your data.
        '''),

        dcc.Dropdown(id='dropdown',
                     options=[
                         {'label': 'Google', 'value': 'GOOG'},
                         {'label': 'Apple', 'value': 'AAPL'},
                         {'label': 'Amazon', 'value': 'AMZN'},
                     ],
                     value='GOOG'),
        dcc.Dropdown(id='dropdown_length',
                     options=[
                         {'label': '1 Month', 'value': '1mo'},
                         {'label': '3 Months', 'value': '3mo'},
                         {'label': '6 Months', 'value': '6mo'},
                         {'label': '1 Year', 'value': '1y'},
                         {'label': '5 Years', 'value': '5y'},
                     ],
                     value='1y'),
        html.Div(children=[
            dcc.Graph(id='line_plot', style={'display': 'inline-block'}),
            dcc.Graph(id='bar_plot', style={'display': 'inline-block'}),
        ])

    ])

    @app.callback(Output(component_id='line_plot', component_property='figure'),
                  [Input(component_id='dropdown', component_property='value'),
                  Input(component_id='dropdown_length', component_property='value'),
                   ])
    def graph_update(dropdown_value, length):
        df = build_dataframe(dropdown_value, length)
        fig = go.Figure([go.Scatter(x=df['Date'], y=df['Close'],
                                    line=dict(color='firebrick', width=4))
                         ])

        fig.update_layout(title='Stock prices over time',
                          xaxis_title='Dates',
                          yaxis_title='Prices'
                          )
        return fig

    @app.callback(Output(component_id='bar_plot', component_property='figure'),
                  [Input(component_id='dropdown', component_property='value'),
                   Input(component_id='dropdown_length', component_property='value'),
                   ])
    def graph_update(dropdown_value, length):
        df = build_dataframe(dropdown_value, length)
        df = format_for_bar(df)
        fig = px.bar(df, x='Month', y='Volume')

        fig.update_layout(title='Average Monthly Volume',
                          xaxis_title='Months',
                          yaxis_title='Volume'
                          )
        return fig




    return app
