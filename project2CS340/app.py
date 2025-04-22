import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from crud import AnimalShelter

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Initialize database connection
db = AnimalShelter("aacuser", "aacpassword")

# Load initial data
initial_data = db.read({})

# App layout
app.layout = dbc.Container([
    # Header with logo
    dbc.Row([
        dbc.Col(html.Img(src=app.get_asset_url('logo.png'), width=2),
        dbc.Col(html.H1("Grazioso Salvare Rescue Animal Dashboard"), width=8),
        dbc.Col(html.Div("Developed by [Your Name]"), width=2)
    ], className="mb-4"),
    
    # Filter controls
    dbc.Row([
        dbc.Col([
            html.H4("Select Rescue Type:"),
            dcc.RadioItems(
                id='rescue-type',
                options=[
                    {'label': 'Water Rescue', 'value': 'water'},
                    {'label': 'Mountain/Wilderness Rescue', 'value': 'mountain'},
                    {'label': 'Disaster/Individual Tracking', 'value': 'disaster'},
                    {'label': 'Reset (Show All)', 'value': 'reset'}
                ],
                value='reset',
                labelStyle={'display': 'block'}
            )
        ], width=3),
        
        # Data table
        dbc.Col([
            dash_table.DataTable(
                id='datatable',
                columns=[{"name": i, "id": i} for i in initial_data.columns],
                data=initial_data.to_dict('records'),
                page_size=10,
                filter_action="native",
                sort_action="native",
                style_table={'overflowX': 'auto'},
                style_cell={
                    'height': 'auto',
                    'minWidth': '100px', 'width': '100px', 'maxWidth': '180px',
                    'whiteSpace': 'normal'
                }
            )
        ], width=9)
    ], className="mb-4"),
    
    # Charts
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='map-graph')
        ], width=6),
        
        dbc.Col([
            dcc.Graph(id='breed-pie-chart')
        ], width=6)
    ])
], fluid=True)

# Callbacks for interactivity
@app.callback(
    [Output('datatable', 'data'),
     Output('map-graph', 'figure'),
     Output('breed-pie-chart', 'figure')],
    [Input('rescue-type', 'value')]
)
def update_dashboard(rescue_type):
    if rescue_type == 'water':
        data = db.get_water_rescue_dogs()
    elif rescue_type == 'mountain':
        data = db.get_mountain_rescue_dogs()
    elif rescue_type == 'disaster':
        data = db.get_disaster_rescue_dogs()
    else:  # reset
        data = db.read({})
    
    # Create map figure
    map_fig = px.scatter_mapbox(
        data,
        lat="location_lat",
        lon="location_long",
        hover_name="name",
        hover_data=["breed", "age_upon_outcome_in_weeks"],
        color_discrete_sequence=["fuchsia"],
        zoom=10,
        height=400
    )
    map_fig.update_layout(mapbox_style="open-street-map")
    map_fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    
    # Create pie chart
    breed_counts = data['breed'].value_counts().reset_index()
    breed_counts.columns = ['breed', 'count']
    pie_fig = px.pie(
        breed_counts.head(10),
        values='count',
        names='breed',
        title='Top 10 Breeds',
        height=400
    )
    
    return data.to_dict('records'), map_fig, pie_fig

if __name__ == '__main__':
    app.run_server(debug=True)