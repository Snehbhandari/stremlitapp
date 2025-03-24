import dash 
from dash import html, dcc 
import pandas as pd 
import plotly.express as px
from dash.dependencies import Input, Output 
from datetime import datetime 
from datetime import timedelta 
import plotly.graph_objects as go

app = dash.Dash(__name__)

# styling 
colors = {
    'full_background': '#FFFFFF',
    'white_bg': '#FFFFFF',
    'container_bg': '#F1F1F1',
    'sidebar': '#d6d6d6',
    'text': '#202020'
}   
spaces = {
    'padding': '10px', 
    'margin':'10px'
}
template = {
    'metric_container': {
        'backgroundColor': colors['white_bg'], 
        'flex': '22%', 
        'padding': spaces['padding'], 
        'textAlign': 'Center'
    }, 
    'big_container': {
        'backgroundColor': colors['white_bg'], 
        'flex': '45%', 
        'padding': spaces['padding'], 
        'textAlign': 'Center'
    }
}
height_div = {
    'big_container': '35vh', 
    'metric_container': '20vh'
} 
graph_colors = {
    'c1': 'orange',
    'c2': 'purple',
    'c3': 'darkblue',
    'c4': 'pink'
}
graph_colors_2 = {
    'Morning': 'orange',
    'Afternoon': 'purple',
    'Evening': 'darkblue',
    'Night': 'pink'
}

# reading data 
df = pd.read_csv('data/calendar_events.csv')
df['Start Date'] = pd.to_datetime(df['Start Date'])
df.reset_index(inplace=True)
# df = df[['Start Date', 'Duration']]

# functions 
def filtered_data(timeline): 
    today = datetime.today()
    
    if timeline == 'Weekly': 
        # Get the past 7 days
        past_week = today - timedelta(days=7)
        updated_df = df[df['Start Date'] >= past_week] 
        updated_df['Day'] = updated_df['Start Date'].dt.strftime('%A')  # Day of the week (e.g., Monday, Tuesday)
        # Add a 'Date' column that shows the date in the desired format
        updated_df['Date'] = updated_df['Start Date'].dt.strftime('%Y-%m-%d')  # Formatted date
        # Combine both 'Date' and 'Day' columns into a new 'Date with Day' column
        updated_df['Date with Day'] = updated_df['Date'] + '<br> (' + updated_df['Day'] + ')'
        updated_df.drop(columns=['Start Date', 'Date', 'Day'], inplace=True) 
        updated_df.rename(columns={'Date with Day': 'Start Date'}, inplace=True) 
        return updated_df

    elif timeline == 'Monthly': 
        # Get the past 30 days
        past_month = today - timedelta(days=30)
        updated_df = df[df['Start Date'] >= past_month]
        updated_df['Week'] = updated_df['Start Date'].dt.to_period('W').apply(lambda r: r.start_time)
        updated_df = updated_df.groupby('Week').agg({'Duration': 'sum'}).reset_index()
        return updated_df

    elif timeline == 'Yearly': 
        # Get the past 365 days
        past_year = today - timedelta(days=365)
        updated_df = df[df['Start Date'] >= past_year]
        updated_df['Month'] = updated_df['Start Date'].dt.to_period('M').apply(lambda r: r.start_time)
        updated_df = updated_df.groupby('Month').agg({'Duration': 'sum'}).reset_index()
        return updated_df

    elif timeline == 'All-time': 
        # Get monthly data for all-time
        updated_df = df
        updated_df['Month'] = updated_df['Start Date'].dt.to_period('M').apply(lambda r: r.start_time)
        updated_df = updated_df.groupby('Month').agg({'Duration': 'sum'}).reset_index()
        return updated_df

    else: 
        updated_df = df 
        return updated_df 

# Metric A - pie chart 
possible_hours_in_day = 14  # 24 hours - 10 hours = 14 hours available per day
possible_hours_in_week = possible_hours_in_day * 7  # Total possible hours in a week
piechart_df = filtered_data('Weekly')
total_actual_hours_worked = piechart_df['Duration'].sum() / 60  # Duration in minutes, convert to hours 
remaining_hours = possible_hours_in_week - total_actual_hours_worked 
# Create the pie chart data 
pie_data = {
    'Category': ['Worked Hours', 'Potential Remaining hours'],
    'Hours': [total_actual_hours_worked, remaining_hours]
} 
pie_df = pd.DataFrame(pie_data) 

# Metric C - Average hours worked per day 
metric_c_df = df
metric_c_df['Start Date'] = pd.to_datetime(metric_c_df['Start Date'])
# Calculate total hours worked (assuming 'Duration' is in minutes, divide by 60 to get hours)
metric_c_df['Worked Hours'] = metric_c_df['Duration'] / 60
# Group by date and sum the worked hours per day
daily_hours = metric_c_df.groupby(metric_c_df['Start Date'].dt.date)['Worked Hours'].sum()
# Calculate average worked hours per day
average_hours_per_day = daily_hours.mean() 

# Metric D - Goal left to achieve (month)
goal = 40  # 40 hours goal 
if total_actual_hours_worked >= goal: 
    goal_left = "Goal Achieved!" 
else: 
    goal_left = goal - total_actual_hours_worked 

# Graph 2 
# categorize time of day 
def categorize_time_of_day(row):
    start_hour = row.hour
    if start_hour >= 6 and start_hour < 11:
        return 'Morning'
    elif start_hour >= 11 and start_hour < 4:
        return 'Afternoon'
    elif start_hour >= 4 and start_hour < 21:
        return 'Evening' 
    else:
        return 'Night' 

# Add a column for Time of Day based on the Start Time 
graph2_df = df
graph2_df['Start Time'] = pd.to_datetime(graph2_df['Start Time'])
graph2_df['Time of Day'] = graph2_df['Start Time'].apply(categorize_time_of_day)
# Group by 'Time of Day' and sum the 'Duration' (which represents worked hours)
graph2_df['Duration'] = graph2_df['Duration'] / 60  # Convert to hours
time_of_day_hours = graph2_df.groupby('Time of Day')['Duration'].sum().reset_index() 
for x in time_of_day_hours['Time of Day'].unique():
    if 'Morning' not in x:
        time_of_day_hours.loc[len(time_of_day_hours)] = ['Morning', 0]
    if 'Afternoon' not in x:
        time_of_day_hours.loc[len(time_of_day_hours)] = ['Afternoon', 0]
    if 'Evening' not in x:
        time_of_day_hours.loc[len(time_of_day_hours)] = ['Evening', 0]
    if 'Night' not in x:
        time_of_day_hours.loc[len(time_of_day_hours)] = ['Night', 0]
    

# layout 
app.layout = html.Div([ 
    # heading 
    html.H1('Time Tracking Dashboard', style={ 'textAlign': 'Center', 
                                           'color': colors['text'], 
                                           'padding': spaces['padding'], 
                                           'backgroundColor': colors['container_bg'],
                                            'margin-bottom': '10px',
                                            'margin-top': '5px'}), 

    html.Div([
    # sidebar 
        html.Div([ 
            # heading 
            html.H2("Time Period", style={'marginTop': spaces['margin'], 'textAlign': 'Center'}), 
            
            # dropdown 
            dcc.Dropdown( 
                id='dropdown-timeline',
                options=[ 
                    {'label': 'Week', 'value': 'Weekly'},
                    {'label': 'Month', 'value': 'Monthly'}, 
                    {'label': 'Year', 'value': 'Yearly'}, 
                    {'label': 'All-Time', 'value': 'All-time'}, 
                ], 
                value = 'Weekly', # default selected value 
                clearable = False
            ), 

            # Explanation of dashboard 

            # Graph 1 
            html.Div([
                html.H4("What is graph 1 showing?"), 
                html.P("Explanation - 1 line "), 
                html.H4("How is the summary generated?"), 
                html.P("AI - chatgpt/ lamma")
            ], style={'backgroundColor': colors['white_bg'], 'padding': '5px', 'marginTop': '10px'}), 

            # Key Metrics 
            html.Div([
                            html.H4("KPIs"), 
                            html.P("Explain KPIs/ Metrics")
                        ], style={'backgroundColor': colors['white_bg'], 'padding': '5px', 'marginTop': '10px'}), 

            html.Div([
                html.H4("Graph 3 and 4"), 
                html.P("Prediction")
            ], style={'backgroundColor': colors['white_bg'], 'padding': '5px', 'marginTop': '10px'})],
            style= {'flex': '1%', 'backgroundColor': colors['sidebar'], 'padding': '10px', 'margin-right': spaces['margin']}),

        # Main Dashboard (80% width)
        html.Div([

            # Title 
            html.H2(id = "varying-title", children = "Variable Name based on Time Period", 
                    style={'marginTop': spaces['margin']}), 

            # A - 2 Containers
            html.Div([ 

                # Graph 1 
                html.Div(dcc.Graph(id = "graph-1", 
                                   style = {"width": "90vh", "height": "32vh"}), style= {**template['big_container'], 'margin-right': spaces['margin'], }),

                # Summary 
                html.Div("Summary", style= {**template['big_container']})

            ], style={'display': 'flex', 'height': height_div['big_container'], 'margin-bottom': spaces['margin']}),
            
            # B - 4 Metrics 
            html.Div([
                    html.Div(dcc.Graph(
                        id='pie-chart-metric-a',
                        figure={
                            'data': [
                                go.Pie(
                                    labels=pie_df['Category'],
                                    values=pie_df['Hours'],
                                    hole=0.3,  # Optional: Makes it a donut chart 
                                    marker=dict(colors=(graph_colors['c2'], graph_colors['c1'])),
                                ),
                            ],
                            'layout': {
                                'title': {
                                    'text': '% hours worked',
                                    'x': 0.5,  # Centering the title
                                    'xanchor': 'center',  # Ensures the title is centered
                                    'y': 0.95,  # Controls the position of the title (you can adjust this)
                                    'yanchor': 'top',  # Position the title at the top
                                    'font': {
                                        'size': 14,  # Adjust title font size
                                        'color': 'black',  # Adjust title font color
                                    }
                                },
                                'showlegend': False, 
                                'height': 180, 
                                # 'width': '5vh',
                                'margin': {'t':35, 'b': 0, 'l': 0, 'r': 0},  # Custom margin values to reduce padding
                                # 'autosize': True,
                                'backgroundColor': colors['sidebar'],
                                'border': '1px black',
                            }
                        }
                    ),
                    style={**template['metric_container'], 'margin-right': spaces['margin']}
                ),
                html.Div([
                    html.Div(id="metric2-title", children="metric2-title"),
                    html.Div(id='sessions-worked', children=f"{len(df)}", style={
                    'fontSize': '100px',  # Large font size
                    'fontWeight': 'bold',
                    'marginTop': '20px',
                    'textAlign': 'center',  # Center the text
                    'justifyContent': 'center',  # Center horizontally
                })
                ], style={**template['metric_container'],
                    'margin-right': spaces['margin'],
                    'display': 'flex', 
                    'flexDirection': 'column'}),
                html.Div([
                    html.Div(id="metric3-title", children="metric3-title"),
                    html.Div(id='metric3', style={
                    'fontSize': '100px',  # Large font size
                    'fontWeight': 'bold',
                    'marginTop': '20px',
                    'textAlign': 'center',  # Center the text
                    'justifyContent': 'center',  # Center horizontally
                })
                ], style={**template['metric_container'],
                    'margin-right': spaces['margin'],
                    'display': 'flex', 
                    'flexDirection': 'column'}), 
                html.Div([
                    html.Div(id="metric4-title", children="metric4 - title"),
                    html.Div(id='metric4', style={
                    'fontSize': '100px',  # Large font size
                    'fontWeight': 'bold',
                    'marginTop': '20px',
                    'textAlign': 'center',  # Center the text
                    'justifyContent': 'center',  # Center horizontally
                })
                ], style= {**template['metric_container']})
                ], style={'display': 'flex', 'height': height_div['metric_container'], 'margin-bottom': spaces['margin']}
            ), 

            # C - 2 Graphs 
            html.Div([

                # Graph 2
                html.Div(html.Div(dcc.Graph(id = "graph-2", 
                                   style = {"width": "68vh", "height": "32vh"}
                                   )),
                                   style= {**template['big_container'], 'margin-right': spaces['margin'], }),

                # Graph 3
                html.Div("Graph 4", style= {**template['big_container']})
                ], style={'display': 'flex', 'height': height_div['big_container']}
            ),

        ], style={'flex': '70%', 'backgroundColor': colors['container_bg'], 'padding': spaces['padding']})

    ] , style={'display': 'flex', 'height': '100vh'})
], style={'backgroundColor': colors['full_background'], 'padding': spaces['padding'], 'margin-top': '0px'})

# defining callbacks 
@app.callback( 
    [Output('graph-1', 'figure'), 
    Output('varying-title', 'children'), 
    Output('metric2-title', 'children'), 
    Output('metric3-title', 'children'), 
    Output('metric3', 'children'), 
    Output('metric4-title', 'children'), 
    Output('metric4', 'children'), 
    Output("graph-2", 'figure')], 
     Input('dropdown-timeline', 'value') 
) 
def update_graph(selected_dropdown_timeline): # takes the value of input in callback 
    if selected_dropdown_timeline is None:
        selected_dropdown_timeline = 'Weekly'
    df_filtered = filtered_data(selected_dropdown_timeline) # function to filter data based on selected value 
    print(df_filtered.head())
    fig = px.bar(df_filtered, x='Start Date', y='Duration', color='Calendar Name') 
    fig.update_layout(
        title=f"Duration Worked",
        margin={'t': 25, 'b': 0, 'l': 0, 'r': 0},  # Adjust the margins as needed 
    )
    title = f"Summary of {selected_dropdown_timeline.capitalize()} Events"
    metric2 = f"Total sessions worked {selected_dropdown_timeline.lower()}"
    metric3_title = f"Average hours worked per day" 
    metric3 = f"{average_hours_per_day:.2f}" 

    if total_actual_hours_worked >= goal: 
        metric4_title = f"Goal Achieved" 
        metric4 = f"Yaay!" 
    else: 
        metric4_title = f"Goal left to achieve (hours)" 
        metric4 = f"{goal_left:.2f}" 
    
    fig_time_of_day = px.bar(time_of_day_hours, x='Time of Day', y='Duration', 
                         title=f"Worked Hours by Time of Day {selected_dropdown_timeline}", 
                         labels={'Duration': 'Total Worked Hours (in hours)', 'Time of Day': 'Time of Day'},
                         color='Time of Day', color_discrete_map=(graph_colors_2))
    fig_time_of_day.update_layout(margin={'t': 25, 'b': 0, 'l': 0, 'r': 0}, showlegend = False)  # Adjust the margins as needed
    
    return fig, title, metric2, metric3_title, metric3, metric4_title, metric4, fig_time_of_day

if __name__ == '__main__': 
    app.run_server(debug=True) 

