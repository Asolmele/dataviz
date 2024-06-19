from dash import Dash, html, dcc, callback, Output, Input

def get_layout():

    title = html.H1(children='4Chan Degeneracy Monitoring Service', style={'textAlign':'center'})

    style = {
        "display" : "flex",
        "align-items" : "center",
        "justify-content" : "center",
        "background-color" : "#FFAFC5"
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
    }

    return html.Div(
        children=[
            get_profanity_layout(),
            get_links_layout()
        ],
        id=id,
        style=style)

def get_profanity_layout():
    style = {
        "display": "flex",
    }
    return html.Div()

def get_links_layout():
    return html.Div()
