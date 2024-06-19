from views import *
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd


app = Dash()

fig = get_figure_message_over_profanity()
app.layout = [
    html.H1(children='Title of Dash App', style={'textAlign':'center'}),
    dcc.Graph(figure=fig),
]

if __name__ == '__main__':
    app.run()
