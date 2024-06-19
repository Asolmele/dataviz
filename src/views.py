from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

import pathlib

res_dir = str(pathlib.Path(
    __file__).parent.parent.resolve().joinpath("results"))

df = pd.read_csv(res_dir + "/result.csv")

df["proportion_profanity"] = df["nb_profanity"] / df["nb_total"]
df["proportion_http"] = df["nb_link_http"] / \
    (df["nb_link_http"] + df["nb_link_https"])
df["proportion_https"] = df["nb_link_https"] / \
    (df["nb_link_http"] + df["nb_link_https"])


def get_figure_message_over_profanity():
    fig = px.scatter(df, x="nb_total", y="nb_profanity", color="board_name",
                     hover_name="board_name", size_max=60)
    fig.update_layout(
        xaxis_title="nombre de messages",
        yaxis_title="nombre de profanités",
        title="nombre de profanités selon le nombre de messages par board"
    )
    return fig


def get_figure_worst_boards():
    fig = px.bar(df, x="board_name", y="proportion_profanity",
                 hover_name="board_name")
    fig.update_layout(
        xaxis_title="board",
        yaxis_title="proportion de profanités",
        title="proportion de profanités par board"
    )
    return fig


def get_figure_less_secure_boards():
    fig = px.pie(df, names="board_name", values="proportion_http")
    fig.update_layout(
        title="Proportion de liens HTTP par board"
    )
    return fig


def get_figure_most_secure_boards():
    fig = px.pie(df, names="board_name", values="proportion_https")
    fig.update_layout(
        title="Proportion de liens HTTPS par board"
    )
    return fig


def get_figure_most_used_site(board_name, min_count=40, nb_max=-1):
    df_board = pd.read_csv(res_dir + f"/link/count/{board_name}.csv")
    if nb_max == -1:
        df_board = df_board[df_board["count"] > min_count]
    else:
        df_board = df_board.nlargest(nb_max, "count")
    fig = px.pie(df_board, names="link", values="count")
    fig.update_layout(
        title=f"Proportion des liens les plus utilisés sur le board {board_name}"
    )
    return fig


def get_worst_board():
    board = df[df["proportion_profanity"] == df["proportion_profanity"].max()]
    board = board.to_dict()
    result = {}
    for key in board.keys():
        key2 = list(board[key].keys())[0]
        result[key] = board[key][key2]
    return result


def get_most_used_thread(board_name):
    board = df[df["board_name"] == board_name]
    text = str(board["most_used_thread"].values[0])
    return text, str(board["nb_thread_used"].values[0])


def get_layout():
    fig = get_figure_message_over_profanity()
    print(get_worst_board())
    return [
        html.H1(children='Title of Dash App', style={'textAlign': 'center'}),
        dcc.Graph(figure=fig),
        dcc.Graph(figure=get_figure_worst_boards()),
        dcc.Graph(figure=get_figure_less_secure_boards()),
        dcc.Graph(figure=get_figure_most_secure_boards()),
        dcc.Graph(figure=get_figure_most_used_site("a", 0, 15)),
        html.H2("Board le plus utilisé"),
    ]
