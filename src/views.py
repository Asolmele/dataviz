from dash import Dash, html, dcc, callback, Output, Input, ctx
import plotly.express as px
import pandas as pd

import pathlib

board_tag_to_names = {
    "a": "Anime & Manga",
    "b": "Random",
    "bant": "International Random",
    "biz": "Business & Finance",
    "ck": "Food & Cooking",
    "co": "Comics & Cartoons",
    "diy": "Do It Yourself",
    "fit": "Fitness",
    "g": "Technology",
    "his": "History",
    "int": "International",
    "jp": "Otaku Culture",
    "k": "Weapons",
    "lit": "Literature",
    "m": "Mecha",
    "mu": "Music",
    "out": "Outdoors",
    "r9k": "ROBOT9001",
    "sci": "Science & Math",
    "trash": "Off-Topic",
    "v": "Video Games",
    "vg": "Video Game Generals",
    "vmg": "Video Games/Mobile",
    "vt": "Virtual YouTubers"
}


res_dir = str(pathlib.Path(
    __file__).parent.parent.resolve().joinpath("results"))

df = pd.read_csv(res_dir + "/result.csv")

df["proportion_profanity"] = df["nb_profanity"] / df["nb_total"]
df["proportion_http"] = df["nb_link_http"] / \
    (df["nb_link_http"] + df["nb_link_https"])
df["proportion_https"] = df["nb_link_https"] / \
    (df["nb_link_http"] + df["nb_link_https"])

ALL_BOARD = ["a", "b", "bant", "biz", "ck", "co", "diy", "fit", "g", "his",
             "int", "jp", "k", "lit", "m", "mu", "out", "r9k", "sci", "trash",
             "v", "vg", "vmg", "vt"]
BOARD_VISIBLE = 0
NB_MIN = 40
NB_MAX = 15


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
    fig.update_layout(
        paper_bgcolor='#FFAFC5'
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


def get_most_used_thread(board_name):
    board = df[df["board_name"] == board_name]
    text = str(board["most_used_thread"].values[0])
    return text, str(board["nb_thread_used"].values[0])


def get_figure_most_used_site(board_name):
    df_board = pd.read_csv(res_dir + f"/link/count/{board_name}.csv")
    if NB_MAX == -1:
        df_board = df_board[df_board["count"] > NB_MIN]
    else:
        df_board = df_board.nlargest(NB_MAX, "count")
    fig = px.pie(df_board, names="link", values="count")
    fig.update_layout(
        title=f"Proportion des liens les plus utilisés sur le board {board_name}"
    )
    return fig


@callback(
    Output("graph-board", "figure"),
    Input("previous_board", "n_clicks"),
    Input("next_board", "n_clicks"),
)
def update_board(n_clicks_previous, n_clicks_next):
    global BOARD_VISIBLE
    if ctx.triggered_id == "previous_board":
        BOARD_VISIBLE -= 1
    if ctx.triggered_id == "next_board":
        BOARD_VISIBLE += 1
    BOARD_VISIBLE = BOARD_VISIBLE % len(ALL_BOARD)
    figure = get_figure_most_used_site(ALL_BOARD[BOARD_VISIBLE])
    figure.update_layout(
        paper_bgcolor='#FFAFC5'
    )
    return figure

@callback(
    Output("p-board", "children"),
    Input("graph-board", "figure"),
)
def update_text_board(figure):
    return get_most_used_thread(ALL_BOARD[BOARD_VISIBLE])[0]


def get_data_one_board():
    return [
        html.Div([
            html.Button("<<", id="previous_board"),
        ], style={"display": "flex", "height": "100%", "margin-left": "0px"}),
        html.Div([
            html.Pre(get_most_used_thread("a")[0], id="p-board", style={
                "text-wrap": "wrap",
            }),
            dcc.Graph(id="graph-board"),
        ], style={"display": "flex", "flex-direction": "column-reverse", "width": "inherit"}),
        html.Div([
            html.Button(">>", id="next_board", style={
                "margin-left": "auto",
                "height": "100%",
            }),
        ], style={"display": "flex", "height": "100%", "margin-right": "0px"}),
    ]


def get_worst_board():
    board = df[df["proportion_profanity"] == df["proportion_profanity"].max()]
    board = board.to_dict()
    result = {}
    for key in board.keys():
        key2 = list(board[key].keys())[0]
        result[key] = board[key][key2]
    return result


def get_profanity_graphs():
    return [
        dcc.Graph(figure=get_figure_message_over_profanity()),
        dcc.Graph(figure=get_figure_worst_boards()),
        dcc.Graph(figure=get_figure_less_secure_boards()),
        dcc.Graph(figure=get_figure_most_secure_boards()),
        dcc.Graph(figure=get_figure_most_used_site("a", 0, 15)),
        html.H2("Board le plus utilisé"),
    ]
