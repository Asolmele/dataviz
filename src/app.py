from views import *
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd


app = Dash()

app.layout = get_layout()

if __name__ == '__main__':
    app.run(debug=True)
