import csv

import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from pandas import Series, DataFrame
#All final race data for each circuit formed into their respective dataframes 
Losail_df = pd.read_csv('Losail_Hour_10.CSV',
                        usecols=['POSITION','NUMBER', 'TEAM', 'VEHICLE','CLASS','LAPS','TOTAL_TIME','GAP_FIRST','FL_TIME'],sep=';')
Imola_df = pd.read_csv('Imola_Hour_6.CSV',
                        usecols=['POSITION','NUMBER', 'TEAM', 'VEHICLE','CLASS','LAPS','TOTAL_TIME','GAP_FIRST','FL_TIME'],sep=';')
Spa_df = pd.read_csv('Spa_Hour_6.CSV',
                        usecols=['POSITION','NUMBER', 'TEAM', 'VEHICLE','CLASS','LAPS','TOTAL_TIME','GAP_FIRST','FL_TIME'],sep=';')
LeMans_df = pd.read_csv('LeMans_Hour_24.CSV',
                        usecols=['POSITION','NUMBER', 'TEAM', 'VEHICLE','CLASS','LAPS','TOTAL_TIME','GAP_FIRST','FL_TIME'],sep=';')
SaoPaulo_df = pd.read_csv('SaoPaulo_Hour_6.CSV',
                        usecols=['POSITION','NUMBER', 'TEAM', 'VEHICLE','CLASS','LAPS','TOTAL_TIME','GAP_FIRST','FL_TIME'],sep=';')
COTA_df = pd.read_csv('COTA_Hour_6.CSV',
                        usecols=['POSITION','NUMBER', 'TEAM', 'VEHICLE','CLASS','LAPS','TOTAL_TIME','GAP_FIRST','FL_TIME'],sep=';')
Fuji_df = pd.read_csv('Fuji_Hour_6.CSV',
                        usecols=['POSITION','NUMBER', 'TEAM', 'VEHICLE','CLASS','LAPS','TOTAL_TIME','GAP_FIRST','FL_TIME'],sep=';')
Bahrain_df = pd.read_csv('Bahrain_Hour_8.CSV',
                        usecols=['POSITION','NUMBER', 'TEAM', 'VEHICLE','CLASS','LAPS','TOTAL_TIME','GAP_FIRST','FL_TIME'],sep=';')
#organizing and sorting the dataframes by fasted lap time so that a total laps vs. fastest lap time scatter plot can be graphed
dataframes_by_fl_time = {
    'Losail': Losail_df.sort_values(by='FL_TIME'),
    'Imola': Imola_df.sort_values(by='FL_TIME'),
    'Spa': Spa_df.sort_values(by='FL_TIME'),
    'LeMans': LeMans_df.sort_values(by='FL_TIME'),
    'Sao Paulo': SaoPaulo_df.sort_values(by='FL_TIME'),
    'Cota': COTA_df.sort_values(by='FL_TIME'),
    'Fuji': Fuji_df.sort_values(by='FL_TIME'),
    'Bahrain': Bahrain_df.sort_values(by='FL_TIME')
}


app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("WEC 2024 Season Dashboard", style={'text-align': 'center'}),

        html.Div([
            #dropdown to select data for a specific circuit
            dcc.Dropdown(
                id='circuit-dropdown',
                options=[
                    {'label': i, 'value': i} for i in dataframes_by_fl_time.keys()],
                placeholder ='Select a circuit',
                value='Losail'
            ),

            dcc.Graph(
                id='fl_time-vs-laps',

            )
        ])
    ])

@app.callback(
    Output('fl_time-vs-laps', 'figure'),
    Input('circuit-dropdown', 'value')
)
#def that allows the dashboard to update the shown graph based on which ciruit is selected by user
def update_graph(selected_circuit):
    df = dataframes_by_fl_time[selected_circuit]
    scatter_fig = px.scatter(df, x='LAPS', y='FL_TIME', title=f'Fastest Lap vs. Total Laps for {selected_circuit}',color='CLASS', hover_name='TEAM')
    return scatter_fig

if __name__ == '__main__':
    app.run_server(debug=True)
