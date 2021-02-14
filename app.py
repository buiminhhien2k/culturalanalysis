import dash
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


backGroundColorOption = html.Div(id = "background",children=[
    html.P("Background Color:"),
    dcc.RadioItems(
        id='background-setting',
        # className="background-setting", 
        options=[{
                "value" : "Dark",
                "label" : "Dark"
                },{
                "value" : "Light",
                "label" : "Light"            
                }
            ],
        value="Light",
    ),
])

countryColorOption = html.Div(id = "country-color",children=[
    html.P("Country Color:"),
    dcc.RadioItems(
        id='country-setting',
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
    ),
])

countryDropDown = dcc.Dropdown(
        id='country-dropdown',
        options= [{"label":country,"value":country} for country in data.country],
        value= "Finland",
        clearable=False
    )

app.layout = html.Div(children=[
    html.H1(children='Cultural Difference from your country',),
    html.Div(children="Dash: A web application framework for Python."),

    html.Br(),
    backGroundColorOption,
    html.Br(),
    countryColorOption,
    html.Br(),
    countryDropDown,
    html.Br(),

    dcc.Graph(id='core-map')
])


@app.callback(
    Output(component_id = "core-map", component_property = 'figure'),
    [
        Input(component_id = 'country-dropdown', component_property= 'value'),
        Input(component_id='background-setting',component_property='value'),
        Input(component_id='country-setting',component_property='value')
    ]
)
def updateMap(country,backgroundMode, countryColor,df = data):
    colorMap = 'totalDiff'
    if country == "":
        country = "Finland"
    metricsList = [ 'pdi', 'idv', 'mas', 'uai', 'ltowvs', 'ivr']
    df[colorMap] = (df[metricsList]-df[df.country == country][metricsList].values).apply(lambda row: row.abs()).sum(axis=1)
    df = df.dropna()
    fig = px.choropleth(
        data_frame=df,
        locations="country",
        locationmode="country names" ,
        color=colorMap,
        range_color=[df[colorMap].min(),df[colorMap].max()],
        hover_data=["country","idv","mas","pdi",'uai', 'ltowvs', 'ivr'],
        color_continuous_scale = countryColor,
        # px.colors.sequential.Plasma
        labels={colorMap:'Total different'}, 
        template = 'xgridoff'
    )
    fig.update_layout(
        autosize=True,
        margin={"r":10,"t":10,"l":10,"b":10},
        )
    if backgroundMode == "Dark":
        fig.update_layout(paper_bgcolor='#4E5D6C')
    else:
        fig.update_layout(paper_bgcolor='#FFFAF0')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)