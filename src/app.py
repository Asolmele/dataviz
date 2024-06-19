from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

from layout import get_layout



app = Dash()

app.layout = get_layout

if __name__ == '__main__':
    app.run(debug=True)
