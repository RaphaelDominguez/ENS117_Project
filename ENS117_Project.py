import csv

import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from matplotlib.pyplot import figure
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
Locations_df = pd.DataFrame({
    'country': ['Qatar', 'Italy', 'Belgium', 'France', 'Brazil', 'USA', 'Japan', 'Bahrain']
})

dataframes = {
    'Losail': Losail_df,
    'Imola': Imola_df,
    'Spa': Spa_df,
    'LeMans': LeMans_df,
    'Sao Paulo': SaoPaulo_df,
    'Cota': COTA_df,
    'Fuji': Fuji_df,
    'Bahrain': Bahrain_df
}

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

dataframes_by_total_time = {
    'Losail': Losail_df.sort_values(by='TOTAL_TIME'),
    'Imola': Imola_df.sort_values(by='TOTAL_TIME'),
    'Spa': Spa_df.sort_values(by='TOTAL_TIME'),
    'LeMans': LeMans_df.sort_values(by='TOTAL_TIME'),
    'Sao Paulo': SaoPaulo_df.sort_values(by='TOTAL_TIME'),
    'Cota': COTA_df.sort_values(by='TOTAL_TIME'),
    'Fuji': Fuji_df.sort_values(by='TOTAL_TIME'),
    'Bahrain': Bahrain_df.sort_values(by='TOTAL_TIME')
}


app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("WEC 2024 Season Dashboard", style={'text-align': 'center'}),

        html.Div([
            #dropdown to select data for a specific circuit
            dcc.Dropdown(
                id='circuit-dropdown',
                options=[
                    {'label': circuit, 'value': circuit} for circuit in dataframes.keys()],
                placeholder ='Select a circuit',
                value='Losail'
            ),

            dcc.Graph(id='fl_time_vs_laps' ),
            dcc.Graph(id='laps_vs_position'),
            dcc.Graph(id='vehicle_types')
        ])
    ])

@app.callback(
    Output('fl_time_vs_laps', 'figure'),
    Input('circuit-dropdown', 'value')
)
#def that allows the dashboard to update the shown graph based on which ciruit is selected by user
def update_scatter_graph(selected_circuit):
    df = dataframes_by_fl_time[selected_circuit]
    fig = px.scatter(df, x='LAPS', y='FL_TIME', title=f'Fastest Lap vs. Total Laps for {selected_circuit}',color='CLASS', hover_name='TEAM')
    return fig

@app.callback(
    Output('laps_vs_position', 'figure'),
    Input('circuit-dropdown', 'value')
)

def update_bar_chart(selected_circuit):
    df2 = dataframes_by_total_time[selected_circuit]
    fig = px.bar(df2, x='POSITION', y='LAPS', title=f'Laps Completed vs. Position {selected_circuit}', color='CLASS', hover_name='TEAM')
    return fig

@app.callback(
    Output('vehicle_types', 'figure'),
    Input('circuit-dropdown', 'value')
)

def update_sunburst(selected_circuit):
    df3 = dataframes[selected_circuit]
    fig = px.sunburst(df3, path=('CLASS', 'VEHICLE'), color='CLASS')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
