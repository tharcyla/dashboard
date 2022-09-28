# import libraries
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output

# import dataset
df = pd.read_csv('data/simulated-data-alt.csv', encoding='latin1')

# convert dates to datetime
# added_date
df['added_date'] = pd.to_datetime(df['added_date'])
# start_date
df['start_date'] = pd.to_datetime(df['start_date'], format="%Y-%m-%d")
# end_date
df['end_date'] = pd.to_datetime(df['end_date'])

# convert real_duration and returns to Int64
df[['real_duration', 'returns']] = df[['real_duration', 'returns']].astype('Int64')

# convert dev to str
df['dev'] = df['dev'].astype(str)
 
external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = Dash(__name__, external_stylesheets=external_stylesheets)

# page title
app.title = "Dashboard"

# dropdown menu containing available developers
dev_dropdown = dcc.Dropdown(options=df['dev'].unique(), value='Agatha')

app.layout = html.Div(
    children=[
        # header block
        html.Div(
            children=[
                html.P(children="📈", className="header-emoji"),
                html.H1(
                    children="Métricas", className="header-title"
                ),
                html.P(
                    children="Analisar o comportamento dos tickets"
                    " que foram direcionados à equipe de desenvolvimento"
                    " entre 2017 and 2022"
                    " (usando dados fictícios)",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        # dropdowns
        html.Div(
            children=[
                # dropdown 1: dev
                html.Div(
                    children=[
                        html.Div(children="Desenvolvedor", className="menu-title"),
                        dcc.Dropdown(
                            id="dev-filter",
                            options=[
                                {"label": dev, "value": dev}
                                for dev in df['dev'].sort_values().unique()
                            ],
                            value="Agatha",
                            clearable=True,
                            className="dropdown",
                        ),
                    ]
                ),
                # dropdown 2: software
                html.Div(
                    children=[
                        html.Div(children="Sistema", className="menu-title"),
                        dcc.Dropdown(
                            id="software-filter",
                            options=[
                                {"label": software, "value": software}
                                for software in df['software'].sort_values().unique()
                            ],
                            value="A",
                            clearable=True,
                            searchable=True,
                            className="dropdown",
                        ),
                    ],
                ),
                # dropdown 4: start date
                html.Div(
                    children=[
                        html.Div(
                            children="Data de Término", className="menu-title"
                        ),
                        dcc.DatePickerRange(
                            id="start-date-range",
                            min_date_allowed=df['end_date'].min().date(),
                            max_date_allowed=df['end_date'].max().date(),
                            start_date=df['end_date'].min().date(),
                            end_date=df['end_date'].max().date(),
                            className="dropdown",
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="dev-chart",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                # html.Div(
                #     children=dcc.Graph(
                #         id="volume-chart",
                #         config={"displayModeBar": False},
                #     ),
                #     className="card",
                # ),
            ],
            className="wrapper",
        ),
    ]
)

@app.callback(
    Output("dev-chart", "figure"),
    [
        Input("dev-filter", "value"),
        Input("software-filter", "value"),
        Input("start-date-range", "start_date"),
        Input("start-date-range", "end_date"),
    ],
)

def update_charts(dev, software, start_date, end_date):
    mask = (
        (df['dev'] == dev)
        & (df['software'] == software)
        & (df['end_date'] >= start_date)
        & (df['end_date'] <= end_date)
    )
    filtered_data = df.loc[mask, :]
    dev_chart_figure = px.histogram(filtered_data,
                                x='end_date', histfunc='avg', 
                                text_auto=True, template='simple_white')
    dev_chart_figure.update_layout(bargap=0.2, yaxis_title="# de Tickets",
                                    xaxis_title="Data de Término",
                                    title={
                                        'text': "Quantidade de Tickets Fechados",
                                        'y': 0.9,
                                        'x': 0.5,
                                        'xanchor': 'center',
                                        'yanchor': 'top'
                                    })
    
    # {
    #     "data": [
    #         {
    #             "x": filtered_data["start_date"],
    #             "y": filtered_data["dev"],
    #             "type": "lines",
    #         },
    #     ],
    #     "layout": {
    #         "title": {
    #             "text": "Quantidade de Tickets Iniciados",
    #         },
    #         "xaxis": {"fixedrange": True},
    #         "yaxis": {"fixedrange": True},
    #         "colorway": ["#17B897"],
    #     },
    # }

    # volume_chart_figure = {
    #     "data": [
    #         {
    #             "x": filtered_data["Date"],
    #             "y": filtered_data["Total Volume"],
    #             "type": "lines",
    #         },
    #     ],
    #     "layout": {
    #         "title": {"text": "Avocados Sold", "x": 0.05, "xanchor": "left"},
    #         "xaxis": {"fixedrange": True},
    #         "yaxis": {"fixedrange": True},
    #         "colorway": ["#E12D39"],
    #     },
    # }
    return dev_chart_figure # volume_chart_figure


if __name__ == "__main__":
    app.run_server(debug=True)