import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output,State
import plotly as py
import plotly.express as px
import pandas as pd
import numpy as np
import sys
import plotly.graph_objects as go

sys.path.insert(0,".")
import preprocessing 

data = preprocessing.culturalMetrics
# countryList = df.country
# countryList = [{"label":country,"value":country} for country in data.country]

# metricsList = [ 'pdi', 'idv', 'mas', 'uai', 'ltowvs', 'ivr']
# df['totalDiff'] = (df[metricsList]-df[df.country == "Finland"][metricsList].values).apply(lambda row: row.abs()).sum(axis=1)
# df = df.dropna()
# df = df[df.country != "Finland"]
# print(countryList)
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__)
server = app.server
# app.scripts.config.serve_locally = False

sidebarObject = html.Div(
  id = 'side-bar'
  , children = [
    #   html.H1("Sidebar"),
      dbc.Nav(
        children= [
            dbc.NavLink("Home", href = "/", active = 'exact'),
            dbc.NavLink("About", href = "/about", active = 'exact'),
            dbc.NavLink("Sources", href = "/sources", active = 'exact'),
            dbc.NavLink("Contact", href = "https://www.linkedin.com/in/hien-minh-bui-311237104/", active = 'exact',target= '_blank')
            ],
        vertical = False,
        pills= True
    )    
  ]
)

backGroundColorOption = html.Div(className = "background-setting",children=[
    html.P("Background Color:",className = "title-options"),
    dcc.Dropdown(
        id = "background-color",
        className='background-setting',
        options=[{
                "value" : "Dark",
                "label" : "Dark"
                },{
                "value" : "Light",
                "label" : "Light"            
                }
            ],
        value="Light",
        clearable=False
    ),
])

countryColorOption = html.Div(className= "country-setting",children=[
    html.P("Country Color:",className = "title-options"),
    dcc.Dropdown(
        id = "country-color",
        className='country-setting',
        # className="background-setting", 
        options=[{
                "value" : "plotly3",
                "label" : "plotly3"
                },{
                "value" : "plasma",
                "label" : "plasma"            
                },{
                "value" : "turbo",
                "label" : "turbo"            
                },{
                "value" : "electric",
                "label" : "electric"            
                },{
                "value" : "hot",
                "label" : "hot"            
                }
            ],
        value="plotly3",
        clearable=False
    ),
])

countryDropDown = html.Div(
    className='country-dropdown',
    children=[
        #className = "title-options",
        html.P("Choose your Country",className = "title-options"),
        dcc.Dropdown(
            id = "country-name",
            className='country-dropdown',
            options= [{"label":country,"value":country} for country in data.country],
            value= "Finland",
            clearable=False
            )
    ]
)
    

app.layout = html.Div(children=[
    dcc.Location(id = 'url'),

    html.Div(
        className = "intro",
        children=[
            html.Div( id = "info-head",
                children=[
                    html.H1(id='title', children='Cultural Difference Analysis project',),
                    html.P(id= "subtitle",children="This analysis will tell you about how other worldwide countries are different from your selected country")
                ]
            ),
            sidebarObject
        ]
    ),

    html.Div(
        id = 'option-setting',
        children=[
            countryDropDown,
            countryColorOption,
            backGroundColorOption
        ]
    ),

    html.Div(id= 'core-content',
        children = [
            html.Div(id = 'text-content', children=[]),
            dcc.Graph(id='core-map'),
            dash_table.DataTable(id = "core-table")
            ]
        )
    ]
)


@app.callback(
    Output(component_id = "core-map", component_property = 'figure'),
    [
        Input(component_id = 'country-name', component_property= 'value'),
        Input(component_id='background-color',component_property='value'),
        Input(component_id='country-color',component_property='value')
    ]
)
def updateMap(country,backgroundMode, countryColor,df = data):
    # borderColor = [1]*df.shape[0]
    colorMap = 'Total different'

    metricsList = [ 'pdi', 'idv', 'mas', 'uai', 'ltowvs', 'ivr']
    df[colorMap] = (df[metricsList]-df[df.country == country][metricsList].values).apply(lambda row: row.abs()).sum(axis=1)
    df = df.dropna().round(2)
    fig = px.choropleth(
        data_frame=df,
        locations="country",
        locationmode="country names" ,
        color=colorMap,
        range_color=[df[colorMap].min(),df[colorMap].max()],
        hover_data=["country","idv","mas","pdi",'uai', 'ltowvs', 'ivr'],
        color_continuous_scale = countryColor,
        # labels={colorMap:'Total different'}, 
        # template = 'xgridoff',
        
    )
    fig.update_layout(
        autosize=True,
        margin={"r":10,"t":10,"l":10,"b":10},
        # paper_bgcolor= "#FFFAF0"
        )
    if backgroundMode == "Dark":
        fig.update_layout(geo_bgcolor='#4E5D6C')
    else:
        fig.update_layout(geo_bgcolor='#FFFAF0')
    return fig

@app.callback(
    [
        Output(component_id = 'core-table', component_property= 'columns'),
        Output(component_id = 'core-table', component_property= 'data')
    ],
    Input(component_id = 'country-name', component_property= 'value')
)
def create_table(country, table = data):
    metricsList = [ 'pdi', 'idv', 'mas', 'uai', 'ltowvs', 'ivr']
    table['Total different'] = (table[metricsList]-table[table.country == country][metricsList].values).apply(lambda row: row.abs()).sum(axis=1)
    table = table.dropna().round(2)

    table_sorted = table.sort_values(['Total different'])
    table_sorted = table_sorted.head(6)[1:]
    columnsList = [{"name":eachColumn, "id":eachColumn} for eachColumn in table_sorted.columns]
    # print(table_sorted.to_dict('records'))
    return columnsList,table_sorted.to_dict('records')

@app.callback(
    Output(component_id = 'text-content', component_property = 'children'),
    [Input(component_id = 'url', component_property = 'pathname')]
)
def content_for_url(pathname):
    if pathname == '/' or pathname == "/home":
        return [html.P('Display some text for Home')]
    if pathname == "/about":
        return [html.P('Display some text for about')]
    if pathname == "/sources":
        return [html.P('Display some text for source')]


    return dbc.Jumbotron(
        [
            html.H1("404: Not found"),
            html.Hr(),
            html.P("your url doesn't exist")
        ]
    )
    # pass
if __name__ == '__main__':
    app.run_server(debug=True)