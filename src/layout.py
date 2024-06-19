from dash import Dash, html, dcc, callback, Output, Input
from views import *


from views import *



def get_layout():

    title = html.H1(children='Service de monitoring de la dégénérescence de 4chan', style={'textAlign':'center'})

    style = {
        "display" : "flex",
        "align-items" : "center",
        "justify-content" : "center",
        "flex-direction": "column",
    }

    layout = html.Div(
        children=[
            title,
            get_main_container()
        ],
        style=style
    )
    return layout

def get_main_container():
    id = "monitor-container"
    style = {
        "display": "flex",
        "flex-direction": "column",
        "min-height" : "500px",
        "background-color" : "#FFCFD2",
        "width" : "100%"
    }

    return html.Div(
        children=[
            get_head_container(),
            get_collumns_container()
        ],
        id=id,
        style=style)


def get_head_container():
    style= {
        "min-height" : "500px",
        "background-color" : "#FFAFC5",
        "max-width" : "100%",
        "margin" : "25px"
    }

    return html.Div(
        children=get_profanity_layout(),
        style=style
    )

def get_profanity_layout():
    #variables
    worst_board = get_worst_board()
    worst_board_name = board_tag_to_names[worst_board["board_name"]]
    worst_ratio = worst_board["nb_profanity"] / worst_board["nb_total"]

    #layout html
    leaderboard =html.Div(
        id="leaderboard",
        children= [
            html.P(
                children=[
                    "Le pire board de 4chan est : ",
                    html.B(worst_board_name),
                    " avec "
                ],
                style={
                    "font-size" : "20px"
                }),
            html.B(
                str(round(worst_ratio * 100, 2)) + "%",
                style={
                    "font-size": "30px"
                }
            ),
            html.P(
                "de tous ses messages contenant au moins 1 insulte",
                style={
                    "font-size" : "20px"
                }),
            html.P("Quelques données..."),
            html.Div(
                children=[
                    html.Div(
                        children = [
                            html.B(str(worst_board["nb_total"])),
                            html.P(" messages envoyés en tout", style={"margin": "3px"})
                        ],
                        style={
                            "margin" : "auto",
                            "width" : "200px",
                            }
                    ),
                    html.Div(
                        children = [
                            html.B(str(worst_board["nb_profanity"])),
                            html.P(" messages contenant des insultes", style={"margin": "3px"})
                        ],
                        style={
                            "margin" : "0 auto",
                            "width" : "200px",
                        }
                    ),
                ],
            style={
                "display" : "flex",
                "margin" : "50px auto"
            })
        ],
        style={
            "font-size" : "20px",
            "text-align" : "center",
            "margin": "0 20px",
        }
    )

    graphs = html.Div(
        children=[

        ],
        style={
            "width" : "100%",
            "max-width" : "100%",
            "margin": "20px"
        },
        id="graphs"
    )

    children = [
        leaderboard,
        graphs
    ]

    #layout style
    style= {
        "display" : "flex",
        "padding" : "30px",

    }

    return html.Div(
        children=children,
        style=style
    )


def get_collumns_container():
    style= {
        "display" : "flex",
        "min-height" : "500px",
        "max-width" : "100%",
    }

    return html.Div(
        children=[
            get_links_layout(),
            get_other_layout(),
        ],
        style=style
    )

def get_links_layout():
    style = {
        "margin" : "25px",
        "background-color" : "#FFAFC5",
        "min-height": "500px",
        "max-width" : "50%",
        "width" : "100%"
    }
    return html.Div(
        style=style
    )

def get_other_layout():
    style = {
        "margin" : "25px",
        "background-color" : "#FFAFC5",
        "max-width" : "50%",
        "min-height": "500px",
        "width" : "100%",
        "display": "flex",
        "flex-direction": "row",
        "align-items": "center",
    }
    return html.Div(
        get_data_one_board(),
        style=style,
    )
