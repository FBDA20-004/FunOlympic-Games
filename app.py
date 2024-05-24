from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Read the dataset
df = pd.read_csv("FunOlympic.csv")

# Create the Dash app
app = Dash(__name__)

server=app.server

# Define the layout of the app
app.layout = html.Div(className='dash-container', children=[
    html.H1("FunOlympics Games Dashboard", className='header'),
    dcc.Tabs(id='tabs', className='nav-tabs', children=[
        dcc.Tab(label='Bar Chart', className='dash-tab', selected_className='tab--selected', children=[
            html.Div(className='tab-bar-chart-content', children=[
                dcc.Dropdown(
                    id='sports-dropdown',
                    className='dash-dropdown',
                    options=[{'label': sport, 'value': sport} for sport in df['sports'].unique()],
                    value='athletics',
                    clearable=False
                ),
                dcc.Graph(id='bar-chart', className='dash-graph'),
            ]),
        ]),
        dcc.Tab(label='Age Distribution Line Graph', className='dash-tab', selected_className='tab--selected', children=[
            html.Div(className='tab-line-graph-content', children=[
                dcc.Dropdown(
                    id='sports-dropdown-line',
                    className='dash-dropdown',
                    options=[{'label': sport, 'value': sport} for sport in df['sports'].unique()],
                    value='athletics',
                    clearable=False
                ),
                dcc.Graph(id='age-distribution-line-graph', className='dash-graph'),
            ]),
        ]),
        dcc.Tab(label='Histogram', className='dash-tab', selected_className='tab--selected', children=[
            html.Div(className='tab-histogram-content', children=[
                dcc.Dropdown(
                    id='Country-dropdown',
                    className='dash-dropdown',
                    options=[{'label': country, 'value': country} for country in df['country'].unique()],
                    value=df['country'].unique()[0],  # Default value
                    clearable=False
                ),
                dcc.Graph(id='histogram-container', className='dash-graph'),
            ]),
        ]),
        dcc.Tab(label='Scatter Plot', className='dash-tab', selected_className='tab--selected', children=[
            html.Div(className='tab-scatter-plot-content', children=[
                dcc.Dropdown(
                    id='country-dropdown-scatter',
                    className='dash-dropdown',
                    options=[{'label': country, 'value': country} for country in df['country'].unique()],
                    value=df['country'].unique()[0],  # Default value
                    clearable=False
                ),
                dcc.Graph(id='scatter-plot', className='dash-graph'),
            ]),
        ]),
        dcc.Tab(label='Heatmap', className='dash-tab', selected_className='tab--selected', children=[
            html.Div(className='tab-heatmap-content', children=[
                dcc.Dropdown(
                    id='country-dropdown-heatmap',
                    className='dash-dropdown',
                    options=[{'label': country, 'value': country} for country in df['country'].unique()],
                    value=df['country'].unique()[0],  # Default value
                    clearable=False
                ),
                dcc.Dropdown(
                    id='sport-dropdown-heatmap',
                    className='dash-dropdown',
                    options=[{'label': sport, 'value': sport} for sport in df['sports'].unique()],
                    value=df['sports'].unique()[0],  # Default value
                    clearable=False
                ),
                dcc.Graph(id='heatmap', className='dash-graph'),
            ]),
        ])
    ])
])

# Define callback to update the bar chart based on dropdown selection
@app.callback(
    Output('bar-chart', 'figure'),
    Input('sports-dropdown', 'value')
)
def update_bar_chart(selected_sport):
    filtered_df = df[df['sports'] == selected_sport]
    fig = px.bar(filtered_df, x='country', y='views', title=f'Views for {selected_sport}')
    return fig

# Define callback to update the line graph based on dropdown selection
@app.callback(
    Output('age-distribution-line-graph', 'figure'),
    Input('sports-dropdown-line', 'value')
)
def update_age_distribution_line_graph(selected_sport):
    filtered_df = df[df['sports'] == selected_sport]
    if filtered_df.empty:
        return go.Figure()
    grouped_df = filtered_df.groupby(['continent', 'country', 'age']).agg({'views': 'sum'}).reset_index()
    if grouped_df.empty:
        return go.Figure()
    figure = go.Figure()
    for continent in grouped_df['continent'].unique():
        continent_df = grouped_df[grouped_df['continent'] == continent]
        figure.add_trace(go.Scatter(x=continent_df['age'], y=continent_df['views'],
                                    mode='lines', name=continent))
    figure.update_layout(title=f'Viewership Distribution by Age for {selected_sport}',
                         xaxis_title='Age', yaxis_title='Total Views', legend_title='Continent')
    return figure

# Define callback to update the histogram based on dropdown selection
@app.callback(
    Output('histogram-container', 'figure'),
    Input('Country-dropdown', 'value')
)
def update_histogram(selected_country):
    filtered_df = df[df['country'] == selected_country]
    updated_fig = px.histogram(filtered_df, x="sports", y="views", color="gender", barmode="group",
                               title=f'Viewership of Sports by Gender in {selected_country}')
    return updated_fig

# Define callback to update the scatter plot based on dropdown selection
@app.callback(
    Output('scatter-plot', 'figure'),
    Input('country-dropdown-scatter', 'value')
)
def update_scatter_plot(selected_country):
    filtered_df = df[df['country'] == selected_country]
    fig = px.scatter(filtered_df, x='occupation', y='views', color='sports', 
                     title=f'Viewership by Occupation and Sports in {selected_country}',
                     labels={'occupation': 'Occupation', 'views': 'Views'})
    return fig

# Define callback to update the heatmap
@app.callback(
    Output('heatmap', 'figure'),
    [Input('country-dropdown-heatmap', 'value'),
     Input('sport-dropdown-heatmap', 'value')]
)
def update_heatmap(selected_country, selected_sport):
    filtered_df = df[(df['country'] == selected_country) & (df['sports'] == selected_sport)]
    grouped_df = filtered_df.groupby('time').agg({'views': 'sum'}).reset_index()
    fig = go.Figure(data=go.Heatmap(x=grouped_df['time'], y=[selected_country], z=[grouped_df['views']], colorscale='Viridis'))
    fig.update_layout(title=f'Viewership Heatmap for {selected_sport} in {selected_country}',
                      xaxis_title='Time', yaxis_title='Country')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
