# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Clean data: drop any rows where critical columns might be missing
spacex_df = spacex_df.dropna(subset=['Launch Site', 'Payload Mass (kg)', 'class'])

# Hardcode stable bounds for the slider
min_payload = 0
max_payload = 10000

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # TASK 1: Dropdown list for Launch Site selection
    dcc.Dropdown(
        id='site-dropdown',
        options=[{'label': 'All Sites', 'value': 'ALL'}] + [
            {'label': str(l), 'value': str(l)} for l in spacex_df['Launch Site'].unique().tolist()
        ],
        value="ALL",
        placeholder="Select a Launch Site here",
        searchable=True
    ),
    html.Br(),

    # TASK 2: Pie chart placeholder
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),
    
    # TASK 3: Slider to select payload range
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
        value=[min_payload, max_payload]
    ),

    # TASK 4: Scatter chart placeholder
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2: Callback function for Pie Chart
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(
            spacex_df, values='class', names='Launch Site',
            title='Total Success Launches By Site'
        )
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        data = filtered_df.groupby('class').size().reset_index(name='class_count')
        fig = px.pie(
            data, values='class_count', names='class',
            title=f'Total Success Launches for site "{entered_site}"'
        )
        return fig

# TASK 4: Callback function for Scatter Plot
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [
        Input(component_id='site-dropdown', component_property='value'),
        Input(component_id='payload-slider', component_property='value')
    ]
)
def get_scatter_plot(entered_site, entered_payload):
    min_value = entered_payload[0]
    max_value = entered_payload[1]
    
    data = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= min_value) &
        (spacex_df['Payload Mass (kg)'] <= max_value)
    ]
    
    if entered_site == 'ALL':
        fig = px.scatter(
            data, x="Payload Mass (kg)", y="class", color="Booster Version Category",
            title='Correlation between Payload and Success for all Sites'
        )
        return fig
    else:
        data = data[data['Launch Site'] == entered_site]
        fig = px.scatter(
            data, x="Payload Mass (kg)", y="class", color="Booster Version Category",
            title=f'Correlation between Payload and Success for site "{entered_site}"'
        )
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)