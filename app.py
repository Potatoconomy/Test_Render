# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import gunicorn
import FunctionGenerator_helper
import FunctionGenerator_Plotting
import path_organizer
import sampling_rate_samd21vPI

# Todo: Have a picture of electrodes appear alongside corresponding graph

app = Dash(__name__)
server = app.server

a_fg = FunctionGenerator_helper.VoltageTimeData(f_path=list(path_organizer.f_fg_dict.keys()))
a_noise = sampling_rate_samd21vPI.VoltageTimeData_NoiseAnalysis(f_path=list(path_organizer.f_noise_dict.keys()))

app.layout = html.Div([
    html.H1("CIAM Dashboard"),
    html.H2("Equipment Characterization"),
    html.Hr(style={"width": "50%", "marginLeft": "25%"}),
    html.H3(
        "Prototype Validation",
        style={"textAlign": "center", "marginTop": "-10px"},
            ),
    html.Hr(style={"width": "50%", "marginLeft": "25%"}),

    dcc.Dropdown(id='function_gen_dropdown',
                 options=[{'label': v, 'value': v} for k, v in path_organizer.f_fg_dict.items()],
                 value=path_organizer.f_fg_titles[0]),

    html.Br(),

    dcc.Graph(id='function_gen_graphs'),

    html.Br(),
    html.Br(),
    html.H2("Noise Characterization"),
    html.Hr(style={"width": "50%", "marginLeft": "25%"}),
    html.H3(
        "Prototype and Electrode Validation",
        style={"textAlign": "center", "marginTop": "-10px"},
            ),
    html.Hr(style={"width": "50%", "marginLeft": "25%"}),

    dcc.Dropdown(id='equipment_noise_dropdown',
                 options=[{'label': v, 'value': v} for k, v in path_organizer.f_noise_dict.items()],
                 value=path_organizer.f_noise_titles[0]),

    html.Br(),

    dcc.Dropdown(id='equipment_noise_filter_dropdown',
                 options=[{'label': v, 'value': v} for v in path_organizer.available_static_filters],
                 value=path_organizer.available_static_filters[0]),

    html.Br(),

    dcc.Graph(id='equipment_noise_graphs'),

    html.Br()

                        ])


@app.callback(Output(component_id='function_gen_graphs', component_property='figure'),
              [Input('function_gen_dropdown', 'value')])
def update_figure(input_value):
    fig = a_fg.make_lineplot_functiongenerator(data=input_value)
    return fig


@app.callback(Output(component_id='equipment_noise_graphs', component_property='figure'),
              [Input('equipment_noise_dropdown', 'value'),
               Input('equipment_noise_filter_dropdown', 'value')])
def update_figure(input_value, filter_input):
    a_noise.filter = filter_input
    fig = a_noise.make_lineplot(data=input_value)
    return fig



if __name__ == '__main__':
    app.run_server(debug=True)
    #a_fg = FunctionGenerator_helper.VoltageTimeData(f_path=list(path_organizer.f_fg_dict.keys()))
    #a_fg.make_lineplot_functiongenerator()
    #a_noise = sampling_rate_samd21vPI.VoltageTimeData_NoiseAnalysis(f_path=list(path_organizer.f_noise_dict.keys()))
    #a_noise.filter = 'Instantaneous Rate of Change (Sampling Rate: 10ms)'
    #a_noise.make_lineplot()