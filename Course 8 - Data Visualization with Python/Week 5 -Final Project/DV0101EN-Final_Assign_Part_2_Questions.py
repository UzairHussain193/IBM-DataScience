#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
app.title = "Automobile Statistics Dashboard"

#---------------------------------------------------------------------------------
# Create the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]

# List of years
year_list = [i for i in range(1980, 2024, 1)]
#---------------------------------------------------------------------------------------
# Create the layout of the app
app.layout = html.Div([
    html.H1("Automobile Statistics Dashboard"),
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='select-statistics',
            options=dropdown_options,
            value='Yearly Statistics',
            placeholder='Select Statistics'
        )
    ]),
    html.Div([
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            value=year_list[0]  # Default to the first year
        )
    ]),
    html.Div([
        html.Div(id='output-container', className='output-container', style={})
    ])
])
#TASK 2.4: Creating Callbacks
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='output-container', component_property='children'),
    Input(component_id='select-statistics', component_property='value'))

def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False
    else:
        return ...

#Callback for plotting
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='select-statistics', component_property='value'),
     Input(component_id='select-year', component_property='value')])

def update_output_container(selected_statistics, input_year):
    if selected_statistics == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = df[df['Recession'] == 1]

        # Plot 1 Automobile sales fluctuate over Recession Period (year wise)
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(
                yearly_rec,
                x='Year',
                y='Automobile_Sales',
                title="Average Automobile Sales fluctuation over Recession Period"
            )
        )

        # Plot 2 Calculate the average number of vehicles sold by vehicle type
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(figure=px.bar(
            average_sales,
            x='Vehicle_Type',
            y='Automobile_Sales',
            title='Average Vehicles Sold by Vehicle Type during Recession'
        ))

        # Plot 3 Pie chart for total expenditure share by vehicle type during recessions
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(figure=px.pie(
            exp_rec,
            values='Advertising_Expenditure',
            names='Vehicle_Type',
            title='Total Expenditure Share by Vehicle Type during Recession'
        ))

        # Plot 4 bar chart for the effect of unemployment rate on vehicle type and sales
        # Assuming you have 'Unemployment_Rate' in your dataset
        unemployment_chart = dcc.Graph(figure=px.bar(
            recession_data,
            x='Unemployment_Rate',
            y='Automobile_Sales',
            color='Vehicle_Type',
            title='Effect of Unemployment Rate on Vehicle Type and Sales during Recession'
        ))

        return [
            html.Div(className='chart-item', children=[html.Div(children=R_chart1), html.Div(children=R_chart2)],
                     style={...}),
            html.Div(className='chart-item', children=[html.Div(children=R_chart3), html.Div(children=unemployment_chart)],
                     style={...})
        ]

    elif (input_year and selected_statistics == 'Yearly Statistics'):
        yearly_data = df[df['Year'] == input_year]

        # Plot 1 Yearly Automobile sales using line chart for the whole period.
        yas = df.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(figure=px.line(
            yas,
            x='Year',
            y='Automobile_Sales',
            title='Yearly Automobile Sales using Line Chart'
        ))

        # Plot 2 Total Monthly Automobile sales using line chart.
        monthly_chart = dcc.Graph(figure=px.line(
            yearly_data,
            x='Month',
            y='Automobile_Sales',
            title='Total Monthly Automobile Sales using Line Chart'
        ))

        # Plot 3 Bar chart for the average number of vehicles sold during the given year
        avg_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(figure=px.bar(
            avg_vdata,
            x='Vehicle_Type',
            y='Automobile_Sales',
            title='Average Vehicles Sold by Vehicle Type in the year {}'.format(input_year)
        ))

        # Plot 4 Pie chart for total advertisement expenditure for each vehicle during the year
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(figure=px.pie(
            exp_data,
            values='Advertising_Expenditure',
            names='Vehicle_Type',
            title='Total Advertisement Expenditure for each Vehicle in the year {}'.format(input_year)
        ))

        return [
            html.Div(className='chart-item', children=[html.Div(children=Y_chart1), html.Div(children=monthly_chart)],
                     style={...}),
            html.Div(className='chart-item', children=[html.Div(children=Y_chart3), html.Div(children=Y_chart4)],
                     style={...})
        ]

    else:
        return None

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)


# %%
