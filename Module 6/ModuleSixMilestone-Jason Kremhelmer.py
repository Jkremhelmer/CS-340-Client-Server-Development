#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Setup the Jupyter version of Dash
from jupyter_dash import JupyterDash

# Configure the necessary Python module imports
import dash_leaflet as dl
from dash import dcc
from dash import html
import plotly.express as px
from dash import dash_table
from dash.dependencies import Input, Output


# Configure the plotting routines
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#### FIX ME #####
# change animal_shelter and AnimalShelter to match your CRUD Python module file name and class name
from CRUD import AnimalShelter



###########################
# Data Manipulation / Model
###########################
# FIX ME update with your username and password and CRUD Python module name. NOTE: You will
# likely need more variables for your constructor to handle the hostname and port of the MongoDB
# server, and the database and collection names

username = "aacuser"
password = "SNHU1234"
shelter = AnimalShelter(username, password)


# class read method must support return of list object and accept projection json input
# sending the read method an empty document requests all documents be returned
df = pd.DataFrame.from_records(shelter.read({}))

# MongoDB v5+ is going to return the '_id' column and that is going to have an 
# invlaid object type of 'ObjectID' - which will cause the data_table to crash - so we remove
# it in the dataframe here. The df.drop command allows us to drop the column. If we do not set
# inplace=True - it will reeturn a new dataframe that does not contain the dropped column(s)
df.drop(columns=['_id'],inplace=True)

## Debug
# print(len(df.to_dict(orient='records')))
# print(df.columns)


#########################
# Dashboard Layout / View
#########################
app = JupyterDash('SimpleExample')

app.layout = html.Div([
    html.Div(id='hidden-div', style={'display':'none'}),
    html.Center(html.B(html.H1('SNHU CS-340 Dashboard'))),
    html.Hr(),
    dash_table.DataTable(
        id='datatable-id',
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns
        ],
        data=df.to_dict('records'),
        edittable=True,
        row_selectable="single", #allows a row to be selected
        selected_rows=[],
        filter_action="native", #allows a filter
        sort_action="native", #allows sorting
        page_action="native", #enable pagination
        page_current=0, #sets start page
        page_size=10, #sets rows per page

    ),
    html.Br(),
     html.Hr(),
     html.Div(
            id='map-id',
            className='col s12 m6',
            )
])

#############################################
# Interaction Between Components / Controller
#############################################
#This callback will highlight a row on the data table when the user selects it
@app.callback(
    Output('datatable-id', 'style_data_conditional'),
    [Input('datatable-id', 'selected_columns')]
)
def update_styles(selected_columns):
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]


# This callback will update the geo-location chart for the selected data entry
# derived_virtual_data will be the set of data available from the datatable in the form of 
# a dictionary.
# derived_virtual_selected_rows will be the selected row(s) in the table in the form of
# a list. For this application, we are only permitting single row selection so there is only
# one value in the list.
# The iloc method allows for a row, column notation to pull data from the datatable
@app.callback(
    Output('map-id', "children"),
    [Input('datatable-id', "derived_virtual_data"),
     Input('datatable-id', "derived_virtual_selected_rows")])
def update_map(viewData, index):
    
    print(virtualRows)
    
    #Austin Animal Center is 30.75, -97.48
    
    if not virtualRows: #builds a default view if no slected lines
        markerArry = (30.75, -97.48) #defult maker for Austin Animal Center
        toolTip = "Austin Animal Center"
        popUpHeading = "Austin Animal Center"
        popUpParagraph = "Shelter Home Location"
        
    else: #Build contextual views
        dff = pd.DataFrame(df.iloc[virtualRows]) #covert to dataframe
        coordLat = float(dff['location_lat'].to_string().split()[1]) #strip ot the Lat
        coordLong = float(dff['location_long'].to_string().split()[1]) #strip out the Long
        markerArray = (coordLat, coordLong) #builds the array based on selection
        
        toolTip = dff['breed']
        popUpHeading = "Animal Name"
        popUpParagraph = dff['name']
        
    return [d1.Map(style={'width': '600px', 'height': '300px'}, center=[30.25,-97.68],
                  zoom=10, children=[d1.TileLayer(id="base-layer-id"),
                                    d1.Marker(postion=markerArray, children=[
                                        d1.Tooltip(toolTip),
                                        d1.Popup([
                                            html.H1(popUpHeading),
                                            html.P(popUpParagraph)
                                        ])
                                    ])
                                ])
           ]
    

app.run_server(debug=True)


# In[ ]:




