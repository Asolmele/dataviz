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
BAD_BOARD = "r9k"
WORST_BOARD_VISIBLE = 16
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
        xaxis_title="Board",
        yaxis_title="Proportion de profanités",
        title="Proportion de profanités par board"
    )
    fig.update_layout(
        paper_bgcolor='#FFAFC5'
    )
    return fig

def get_figure_boards_messages():
    fig = px.bar(df, x="board_name", y="nb_total",
                 hover_name="board_name")
    fig.update_layout(
        xaxis_title="board",
        yaxis_title="Nombre total de messages",
        title="Nombre total de messages par board"
    )
    fig.update_layout(
        paper_bgcolor='#FFAFC5'
    )
    return fig
def get_figure_boards_profanity():
    fig = px.bar(df, x="board_name", y="nb_profanity",
                    hover_name="board_name")
    fig.update_layout(
        xaxis_title="board",
        yaxis_title="Nombre total de messages",
        title="Nombre total de messages contenant des profanités par board"
    )
    fig.update_layout(
        paper_bgcolor='#FFAFC5'
    )
    return fig

def get_figure_less_secure_boards():
    fig = px.pie(df, names="board_name", values="proportion_http")
    fig.update_layout(
        title="Proportion de liens HTTP par board",
        paper_bgcolor='#FFAFC5'
    )
    return fig


def get_figure_most_secure_boards():
    fig = px.pie(df, names="board_name", values="proportion_https")
    fig.update_layout(
        title="Proportion de liens HTTPS par board",
        paper_bgcolor='#FFAFC5'
    )
    return fig


def get_most_used_thread_all():
    board = df[df["nb_thread_used"] == df["nb_thread_used"].max()]
    text = str(board["most_used_thread"].values[0])
    return text, str(board["nb_thread_used"].values[0])


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
        title=f"Proportion des liens les plus utilisés sur le board {board_tag_to_names[board_name]}"
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
            html.Div(
                children=[
                    html.Div([
                        html.Button("<<", id="previous_board"),
                    ], style={"display": "flex", "height": "50%", "margin-left": "0px", "align-self": "center"}),
                    dcc.Graph(id="graph-board"),
                    html.Div([
                        html.Button(">>", id="next_board", style={
                            "margin-left": "auto",
                            "height": "50%",
                            "align-self": "center"
                        }),
                    ], style={"display": "flex", "height": "100%", "margin-right": "0px"}),
                ],
                style={
                    "display": "flex",
                    "height": "600px",
                    "justify-content": "space-around",
                    "padding": "20px"
                }
            ),
            html.P("Le message ayant généré le plus de réponses est: ", style={"text-align": "center", "padding": "10px", "font-size": "20px"}),
            html.Pre(
                get_most_used_thread("a")[0],
                style= {
                    "text-align" : "center",
                    "border": "solid #7B435B",
                    "background-color" : "whitesmoke",
                    "margin" : "20px",
                    "text-wrap": "wrap",
                    "padding": "20px"
                },
                id="p-board"
            )
        ], style={"display": "flex", "flex-direction": "column", "width": "100%", "height": "100%"}),
    ]


def get_worst_board():
    board = df[df["proportion_profanity"] == df["proportion_profanity"].max()]
    board = board.to_dict()
    result = {}
    for key in board.keys():
        key2 = list(board[key].keys())[0]
        result[key] = board[key][key2]
    return result


def get_board(index):
    board = df.iloc[index].to_dict()
    result = {}
    for key in board.keys():
        result[key] = board[key]
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


@callback(
    [
        Output("worst_board_link", "children"),
        Output("worst_board", "children"),
        Output("nb_total", "children"),
        Output("nb_profanity", "children"),
        Output("worst_ratio", "children"),
    ],
    Input("worst_board_link", "n_clicks"),
    prevent_initial_call=True
)
def update_board_link(n_clicks):
    global WORST_BOARD_VISIBLE
    WORST_BOARD_VISIBLE += 1
    WORST_BOARD_VISIBLE = WORST_BOARD_VISIBLE % len(ALL_BOARD)
    data = get_board(WORST_BOARD_VISIBLE)
    text = "L'un des board de 4chan est : "
    if WORST_BOARD_VISIBLE == BAD_BOARD:
        text = "Le pire board de 4chan est : "
    worst_ratio = data["nb_profanity"] / data["nb_total"]
    return [
        text,
        board_tag_to_names[data["board_name"]],
        data["nb_total"],
        data["nb_profanity"],
        str(round(worst_ratio * 100, 2)) + "%",
    ]
