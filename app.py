# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

app = dash.Dash(__name__)
server = app.server
app.title = "SJ Charts"
app.scripts.config.serve_locally = True

# Custom CSS and Google Site Tag
external_css = "https://cdn.rawgit.com/aakashhdesai/e75cf352e52c3db6ef1ee36167636001/raw/799da80ffb789ca2e7250afcec5a82c9c65ca55f/style.css"
app.css.append_css({
    "external_url": external_css
})

# Get the RAW CSV
csv = "https://raw.githubusercontent.com/codeforsanjose/sj-data-charts/master/sj_economics_monthly_2006_2016.csv"

# Reads the csv and analyzes the dataframe
def analyze_jobs_frame():

    # Get the raw data from a csv import
    jobs = pd.read_csv(csv)

    # Initialize the data to work with
    work_frame = pd.DataFrame({})
    only_jobs_time = jobs.groupby(jobs["Year"].between(2008,2015, inclusive=True), as_index = False)

    # Annualize and analyze
    for year in range(2008,2015 + 1):
        work_frame = work_frame.append(only_jobs_time.apply(lambda x: x[x['Year'] == year]).mean().round(), ignore_index=True)

    return work_frame

def analyze_unemployment_frame():

    # Get the raw data from a csv import
    unemployment = pd.read_csv(csv)
    
    # Initialize the data to work with
    unemployment_frame = pd.DataFrame({})
    only_unemployment_time = unemployment.groupby(unemployment["Year"].between(2008,2015, inclusive=True), as_index = False)["Year", "SJ Unemployment", "SJ Metro Unemployment"]
    
    for year in range(2006,2016 + 1):
        unemployment_frame = unemployment_frame.append(only_unemployment_time.apply(lambda x: x[x['Year'] == year]).mean(), ignore_index=True)
    
    return unemployment_frame

def get_jobs_table(dataframe):

    table_frame = dataframe.filter(regex="Jobs$", axis=1)

    return table_frame

def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

# Call analysze frame as needed

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    
    html.Div(children=[
        html.Div(id='topnav', children=[
            dcc.Link('Jobs by Sector', href='/'),
            dcc.Link('Unemployment', href='/unemployment'),
            dcc.Link('Housing', href='/housing')
        ]),
        
        html.Div(id='page-content'),
        
        html.Div(children=[
            html.A(html.Button('Data'),
                href='https://github.com/aakashhdesai/sj-data-analysis',
            ),
            
            html.I(
                '  Made with <3 in the City of San Jose.'
            )
        ])
    ])
])

df = analyze_jobs_frame()
main = html.Div(children=[
    
    # Set a Title for the Page
    html.H2(id='dashboard-title',children=[
        'San Jose Jobs by Sector'
    ]),

    # Generate the Jobs by Sector graph from the dataframe constructed in analyze_frame()
    dcc.Graph(
        id='sj-jobs-sector-graph',
        figure={
            'data': [
                {'x': df["Year"], 'y': df["Construction Jobs"], 'type': 'line', 'name': 'Construction Jobs', 'value': 'C'},
                {'x': df["Year"], 'y': df["Education and Health Services Jobs"], 'type': 'line', 'name': 'Education and Health Services Jobs', 'value': 'EHS'},
                {'x': df["Year"], 'y': df["Financial Activities Jobs"], 'type': 'line', 'name': 'Financial Activities Jobs', 'value': 'FA'},
                {'x': df["Year"], 'y': df["Information Jobs"], 'type': 'line', 'name': 'Information Jobs', 'value': 'I'},
                {'x': df["Year"], 'y': df["Leisure and Hospitality Jobs"], 'type': 'line', 'name': 'Leisure and Hospitality Jobs', 'value': 'LH'},
                {'x': df["Year"], 'y': df["Manufacturing Jobs"], 'type': 'line', 'name': 'Manufacturing Jobs', 'value': 'M'},
                {'x': df["Year"], 'y': df["Natural Resources and Mining Jobs"], 'type': 'line', 'name': 'Natural Resources and Mining Jobs', 'value': 'NRM'},
                {'x': df["Year"], 'y': df["Other Services Jobs"], 'type': 'line', 'name': 'Other Services Jobs', 'value': 'OS'},
                {'x': df["Year"], 'y': df["Professional and Business Services Jobs"], 'type': 'line', 'name': u'Professional and Business Services Jobs', 'value': 'PBS'},
                {'x': df["Year"], 'y': df["Public Administration Jobs"], 'type': 'line', 'name': 'Public Administration Jobs', 'value': 'PA'},
                {'x': df["Year"], 'y': df["Trade, Transportation and Utilities Jobs"], 'type': 'line', 'name': u'Trade, Transportation and Utilities Jobs', 'value': 'TTU'},
                {'x': df["Year"], 'y': df["Unclassified Jobs"], 'type': 'line', 'name': 'Unclassified Jobs', 'value': 'U'},
            ],
            'layout': {
                'font': {
                'showlegend': 'False'
                }
            }
        },
        config={
            'displayModeBar': False
        }
    ),
])

housing = html.Div(children=[
    # Set a Title for the Page
    html.H2(id='dashboard-title',children=[
        'San Jose Housing Prices'
    ]),
    
    html.H1(
        'Coming Soon!',
        style={
            'textAlign': 'center',
            'font': 'Helvetica',
            'font-size': '72px',
            'margin': '130px'
        }
    )
])

uf = analyze_unemployment_frame()
unemployment = html.Div(children=[
    # Set a Title for the Page
    html.H2(id='dashboard-title',children=[
        'San Jose Unemployment'
    ]),
    
    # Plot the unemployment graph
    dcc.Graph(
        id='sj-jobs-sector-graph',
        figure={
            'data': [
                {'x': uf["Year"], 'y': uf["SJ Unemployment"], 'type': 'line', 'name': 'Unemployment'},
                {'x': uf["Year"], 'y': uf["SJ Metro Unemployment"], 'type': 'line', 'name': 'Metro Unemployment'},
                ],
                'layout': {
                    'font': {
                    'showlegend': 'False'
                    }
                }
            },
            config={
                'displayModeBar': False
            }
    ),
])

# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/housing':
        return housing
    elif pathname == '/unemployment':
        return unemployment
    else:
        return main


if __name__ == '__main__':
    app.run_server(debug=True)
