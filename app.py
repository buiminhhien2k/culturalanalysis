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
# import plotly.graph_objects as go
from sklearn.cluster import KMeans

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
    
legendMode = html.Div(
    className = 'legend-mode',
    children=[
        html.P('Display Mode:', className='title-options'),
        dcc.Dropdown(
            id= 'legend',
            className='legend-mode',
            options=[
                {"label":'Continuous',"value":'Continuous'},
                {"label":'Clustered',"value":'Clustered'}],
            value= 'Continuous',
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
            legendMode,
            countryColorOption,
            backGroundColorOption,
        ]
    ),

    html.Div(id= 'core-content',
        children = [
            html.Div(id = 'text-content', children=[]),
            dcc.Graph(id='core-map'),
            html.I(id= 'note'),
            html.Br(),
            html.Hr(),
            html.H3(id = 'core-table-title'),
            dash_table.DataTable(id = "core-table")
            ]
        )
    ]
)
def clusterData(dataframe, newCol, valueCol, countryExcept, clusterNum = 5):
    #return new dataframe
    model = KMeans(n_clusters=clusterNum, random_state=0)
    dataframe[newCol] = "0"
    countryExceptRow = dataframe[dataframe['country'] == countryExcept]
    dataframe = dataframe[dataframe['country'] != countryExcept]
    dataframe[newCol] = model.fit(dataframe[valueCol].to_frame()).labels_
    data= dataframe.groupby(newCol)[valueCol].mean().sort_values()
    transformedIndex = {}
    for i in range(clusterNum):
        transformedIndex[data.index[i]]= str(i)

    dataframe.replace(transformedIndex,inplace= True)
    dataframe = dataframe.append(countryExceptRow)

    return dataframe.sort_values(newCol)
@app.callback(
    Output(component_id = "core-map", component_property = 'figure'),
    [
        Input(component_id = 'country-name', component_property= 'value'),
        Input(component_id='background-color',component_property='value'),
        Input(component_id='country-color',component_property='value'),
        Input(component_id='legend',component_property='value')
    ]
)
def updateMap(country,backgroundMode, countryColor,legendMode ,df = data):
    # borderColor = [1]*df.shape[0]
    colorMap = 'Total different'
    metricsList = [ 'pdi', 'idv', 'mas', 'uai', 'ltowvs', 'ivr']
    df[colorMap] = (df[metricsList]-df[df.country == country][metricsList].values).apply(lambda row: row.abs()).sum(axis=1)
    df = df.dropna().round(2)
    if legendMode == "Clustered":
        groupColumn = "Clustered Group"
        df = clusterData(df,groupColumn, "Total different",country)
        colorMap = groupColumn
    fig = px.choropleth(
        data_frame=df,
        locations="country",
        locationmode="country names" ,
        color=colorMap ,
        range_color=[df[colorMap].min(),df[colorMap].max()],
        hover_data=["country","idv","mas","pdi",'uai', 'ltowvs', 'ivr'],
        color_continuous_scale = countryColor,
        # color_discrete_sequence = ['blue','red','green','purple','orange'],
        # labels={colorMap:'Total different'}, 
        # template = 'xgridoff',
        
    )
    # if legendMode == "Continuous":
    #     fig.update_geos (
    #         countrycolor = 'palegoldenrod',
    #     )
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
    Output(component_id='note',component_property='children'),    
    Input(component_id='legend',component_property='value')
)
def uploadNote(legendMode):
    if legendMode == "Clustered":
        return "The higher number of the group, the more different that group is to your selected country"
    return ""

@app.callback(
    [
        Output(component_id = 'core-table-title', component_property= 'children'),
        Output(component_id = 'core-table', component_property= 'columns'),
        Output(component_id = 'core-table', component_property= 'data')
    ],
    Input(component_id = 'country-name', component_property= 'value')
)
def create_table(country, table = data):
    title = "Top 5 countries having the most similar cultures to " + country
    metricsList = [ 'pdi', 'idv', 'mas', 'uai', 'ltowvs', 'ivr']
    table['Total different'] = (table[metricsList]-table[table.country == country][metricsList].values).apply(lambda row: row.abs()).sum(axis=1)
    table = table.dropna().round(2)

    table_sorted = table.sort_values(['Total different'])
    table_sorted = table_sorted.head(6)[1:]
    columnsList = [{"name":eachColumn, "id":eachColumn} for eachColumn in table_sorted.columns]
    # print(table_sorted.to_dict('records'))
    return title, columnsList, table_sorted.to_dict('records')

@app.callback(
    Output(component_id = 'text-content', component_property = 'children'),
    [Input(component_id = 'url', component_property = 'pathname')]
)
def content_for_url(pathname):
    if pathname == '/' or pathname == "/home":
        return [dcc.Markdown('''
            This project is inspired and developed more from a subject, Data Analytics 3, 
            I studied in Lapland University of Applied Sciences, also my home university.

            The original project is to work with **M Language** and **DAX** in **Power BI** to get used to analyzing data, 
            but I want to make the dashboard more interesting and accessible by 
            redoing them as my personal project with Python Dash plotly framework.
            '''
        )]
    if pathname == "/about":
        return [dcc.Markdown('''
        I used callback function in Plotly/Dash framework to create interactive graphs 
        and CSS and Bootstraps to design layout of the websites. I also used Clustering algorithm to
        group the countries based on the cultural difference index.
            
        ** How I calculate the cultural difference index:**

        1. Fill the missing cultural index by calculating the adjacent/neigbour countries to it.
        2. Calculate the difference by add up all the absolute of difference of each index in each country 
        and each index in your chosen country
        3. Apply Machine Learning clustering method (KMeans algorithm) to define the countries group having the smallest difference 
        from you chosen one.
            ''')]
    if pathname == "/sources":
        return [dcc.Markdown('''
        ** Data Sources:**

        1. Six metrics to measure a culture of a country: https://geerthofstede.com/research-and-vsm/dimension-data-matrix/
            - Description: containing 6 metrics indicate the culture of a countries \[`pdi`, `idv`, `mas`, `uai`, `ltowvs`, `ivr`\]
        2. Country and its bordering countries: https://en.wikipedia.org/wiki/List_of_countries_and_territories_by_land_borders
            - Description: listing all the adjacent/neighbouring countries of a country.
            
        ** Document source:**

        1. Dash plotly official website/document: https://dash.plotly.com/
            - Description: I have all my neccessary information to build this project through this source.
        2. Bootstrap with dash plotly official website/document: https://dash-bootstrap-components.opensource.faculty.ai/docs/
            - Description: I learned about Bootstrap fundamental manipulation to layout the website.
            ''')]


    return dbc.Jumbotron(
        [
            html.H1("404: Not found"),
            html.Hr(),
            html.P("your url doesn't exist")
        ]
    )
if __name__ == '__main__':
    app.run_server(debug=True)