import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta 
import plotly.graph_objects as go
from datetime import datetime

# Sample data (replace with loading your actual CSV file)


# Load the data
df = pd.read_csv('data/calendar_events.csv')

# preprocessing 
# drop irrelevant column 
df.drop(columns = 'Event ID', inplace = True)
# converting everything to hours. 
df['Duration_hrs'] = df['Duration']/60

# dataset for PLOT 1
work_df = df[(df["Calendar Name"] == "Job Applications") | (df["Calendar Name"] == "projects")]
# Create a new DataFrame with the count of occurrences of each date in "Start Date"
new_df = work_df['Start Date'].value_counts().reset_index()
new_df.sort_values(by='Start Date', inplace=True)
# Rename columns for clarity
new_df.columns = ['Start Date', 'Count Events']

fig = go.Figure()
# Map each unique value in 'Calendar Name' to a color
calendar_names = work_df["Calendar Name"].unique()
color_map = {name: color for name, color in zip(calendar_names, ['violet', 'pink'])}
# Add the bar plot
fig.add_trace(go.Bar(x=work_df["Start Date"], y=work_df["Duration_hrs"], name="hours worked", marker=dict(
        color=[color_map[name] for name in work_df["Calendar Name"]]),  # custom colors based on 'Calendar Name'
        hovertemplate='<b>Date:</b> %{x}<br><b>Hours Worked:</b> %{y}<br><b>Work category:</b> %{customdata}<extra></extra>',  # Custom hover info
        customdata=work_df["Calendar Name"],  # Pass the Calendar Name as custom data
))
    
# add line for threashold 
fig.add_trace(go.Scatter(x=work_df["Start Date"], y=[7] * (len(work_df)), mode="lines", name="goal", line=dict(color="lightgreen", dash="solid")))
fig.add_trace(go.Scatter(x=new_df["Start Date"],  y=new_df["Count Events"], mode="lines", name="number of events", line=dict(color="red", dash="solid")))
fig.update_layout( 
    plot_bgcolor="lightgoldenrodyellow",  # Clean background
    paper_bgcolor="lightgoldenrodyellow",  # Ensures outer area also matches
    xaxis_title="Date",
    yaxis_title="Hours Worked",
    title=dict(
        text="Hours Worked Per Day",
        x=0.5,  # Centers the title
        xanchor='center',  # Ensures proper alignment 
    ),
    yaxis=dict(range=[0, 10]),  # Set Y-axis range (Adjust values as needed)
    margin=dict(l=20, r=20, t=40, b=40),  # Adjust margins
    font=dict(size=14),
    showlegend=False
)

# METRICS 
# Largest Event 
a =work_df.sort_values(by = "Duration").head().iloc[0,:]
day_of_week = datetime.strptime(a['Start Date'], '%Y-%m-%d').strftime('%A')  # Extract day of the week from 'Start Date'
start_time = datetime.strptime(a['Start Time'], '%H:%M:%S').strftime('%H:%M')  # Format 'Start Time' to hours and minutes
formatted_string = f"Day: {day_of_week} \nTime: {start_time}\nHours: {a['Duration_hrs']}\nPurpose: {a['Calendar Name']}"



# Initialize the Dash app 
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP]) 

# App layout with improved styling
app.layout = html.Div(
    style={'backgroundColor': '#f5f5dc', 'padding': '20px'},  # Cream background color
    children=[
        html.H1("Work Dashboard", style={'textAlign': 'center', 'color': '#343a40'}),  # Title

        html.Div([
            dcc.Graph(figure=fig)  # Display Plotly graph
        ], style={  # Bordered container
            "border": "4px solid #ddd",
            "border-radius": "10px",
            "padding": "10px",
            "box-shadow": "2px 2px 10px rgba(0, 0, 0, 0.1)",
            "background-color": "lightgoldenrodyellow",
            "width": "60%",
            "margin": "5px"
        }),


        # Metrics Section (example)
        html.Div([
            dbc.Row([
                # First metric
                dbc.Col(
                    html.Div([
                        html.H5("Total Sessions", style={'textAlign': 'center', 'color': '#343a40'}),
                        html.H4(f"{df.shape[0]}", style={'textAlign': 'center', 'color': '#007bff'})
                    ], style={"border": "2px solid #ddd", "border-radius": "10px", "padding": "10px", "background-color": "lightgoldenrodyellow"}),
                    width=3  # Adjust column width (1/4th of the row)
                ),
                
                # Second metric
                dbc.Col(
                    html.Div([
                        html.H5("Largest Event", style={'textAlign': 'center', 'color': '#343a40'}),
                        html.P(formatted_string, style={'textAlign': 'center', 'color': '#007bff'})
                    ], style={"border": "2px solid #ddd", "border-radius": "10px", "padding": "10px", "background-color": "lightgoldenrodyellow"}),
                    width=3  # Adjust column width (1/4th of the row)
                ),
                
                # Third metric
                dbc.Col(
                    html.Div([
                        html.H5("Metric 3", style={'textAlign': 'center', 'color': '#343a40'}),
                        html.H4("Value 3", style={'textAlign': 'center', 'color': '#007bff'})
                    ], style={"border": "2px solid #ddd", "border-radius": "10px", "padding": "10px", "background-color": "lightgoldenrodyellow"}),
                    width=3  # Adjust column width (1/4th of the row)
                ),
                
                # Fourth metric
                dbc.Col(
                    html.Div([
                        html.H5("Metric 4", style={'textAlign': 'center', 'color': '#343a40'}),
                        html.H4("Value 4", style={'textAlign': 'center', 'color': '#007bff'})
                    ], style={"border": "2px solid #ddd", "border-radius": "10px", "padding": "10px", "background-color": "lightgoldenrodyellow"}),
                    width=3  # Adjust column width (1/4th of the row)
                ),
            ]),
        ], style={"margin-top": "30px"}),

        # A Call-to-action Button (Example: Apply to a job)
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H4("Apply to a job, it takes 6 seconds", style={'color': '#343a40'}),
                    dbc.Button("Apply to a Job", color="success", href="https://www.glassdoor.com", target="_blank")
                ]),
                width=12, style={'textAlign': 'center'}
            ),
        ], style={'marginBottom': '60px', "margin-top": "30px"}),


        # Footer Section
        html.Div(
            children=[
                html.P("Powered by Dash and Plotly", style={'textAlign': 'center', 'fontSize': '14px', 'color': '#6c757d'}),
            ],
            style={'marginTop': '30px', 'paddingTop': '20px'}
        )
    ]
)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
