import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
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
    html.Center(
        className = "intro",
        children=[
            html.H1(children='Cultural Difference from your country',),
            html.Div(id= "subtitle",
                children="Dash: A web application framework for Python."),
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
    # html.Br(),

    dcc.Graph(id='core-map'),
    dash_table.DataTable(id = "core-table")
    # columns=[ 'pdi', 'idv', 'mas', 'uai', 'ltowvs', 'ivr'],)
])


@app.callback(
    Output(component_id = "core-map", component_property = 'figure'),
    [
        Input(component_id = 'country-name', component_property= 'value'),
        Input(component_id='background-color',component_property='value'),
        Input(component_id='country-color',component_property='value')
    ]
)
def updateMap(country,backgroundMode, countryColor,df = data):
    borderColor = [1]*df.shape[0]
    colorMap = 'totalDiff'

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
        labels={colorMap:'Total different'}, 
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
    
    
    # pass
if __name__ == '__main__':
    app.run_server(debug=True)