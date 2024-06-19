from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

import pathlib

res_dir = str(pathlib.Path(__file__).parent.parent.resolve().joinpath("results"))

df = pd.read_csv(res_dir + "/result.csv")

def get_figure_message_over_profanity():
    fig = px.scatter(df, x="nb_total", y="nb_profanity", size="nb_word_total", color="board_name",
        hover_name="board_name", size_max=60)
    return fig
