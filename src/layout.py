from dash import Dash, html, dcc, callback, Output, Input
from views import *


def get_layout():

    title = html.H1(children='4Chan Degeneracy Monitoring Service', style={'textAlign':'center'})

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

def get_profanity_layout():
    style = {
        "background-color" : "#FFAFC5",

    }
    return html.Div()

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
