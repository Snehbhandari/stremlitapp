import dash 
from dash import html, dcc 

app = dash.Dash(__name__)

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
    }
}

app.layout = html.Div([
    # heading 
    html.H1('Dashboards with Dash', style={ 'textAlign': 'Center', 
                                           'color': colors['text'], 
                                           'padding': spaces['padding'], 
                                           'backgroundColor': colors['container_bg'],
                                            'margin-bottom': '10px',
                                            'margin-top': '5px'}), 

    html.Div([
    # sidebar 
        html.Div([html.H2("Sidebar", style={'marginTop': spaces['margin'], 'textAlign': 'Center'})], 
                 style= {'flex': '2%','backgroundColor': colors['sidebar'], 'padding': '10px', 'margin-right': spaces['margin']}),

    # Main Dashboard (80% width)
        html.Div([

            # Title 
            html.H2("Container 1", style={'marginTop': spaces['margin'], 'textAlign': 'Center'}), 

            # A - 2 Containers 
            html.Div([

                # Graph 1 
                html.Div("Graph 1", style= {'backgroundColor': colors['white_bg'], 'flex': '45%', 'margin-right': spaces['margin'], 'padding': spaces['padding'], 'textAlign': 'Center'}),

                # Summary 
                html.Div("Summary", style= {'backgroundColor': colors['white_bg'], 'flex': '45%', 'padding': spaces['padding'], 'textAlign': 'Center'})

            ], style={'display': 'flex', 'height': '35vh', 'margin-bottom': spaces['margin']}),
            
            # B - 4 Metrics 
            html.Div([
                html.Div("Metric A", style= {**template['metric_container'], 'margin-right': spaces['margin']}),
                html.Div("Metric B", style= {**template['metric_container'], 'margin-right': spaces['margin']}), 
                html.Div("Metric C", style= {**template['metric_container'], 'margin-right': spaces['margin']}),
                html.Div("Metric D", style= {**template['metric_container']})
                ], style={'display': 'flex', 'height': '20vh', 'margin-bottom': spaces['margin']}
            ), 

            # C - 2 Graphs 
            html.Div([

                # Graph 3
                html.Div("Graph 3", style= {'backgroundColor': colors['white_bg'], 'flex': '45%', 'margin-right': spaces['margin'], 'padding': spaces['padding'], 'textAlign': 'Center'}),

                # Graph 4
                html.Div("Graph 4", style= {'backgroundColor': colors['white_bg'], 'flex': '45%', 'padding': spaces['padding'], 'textAlign': 'Center'})
                ], style={'display': 'flex', 'height': '35vh'}
            ),

        ], style={'flex': '70%', 'backgroundColor': colors['container_bg'], 'padding': spaces['padding']})

    ] , style={'display': 'flex', 'height': '100vh'})
], style={'backgroundColor': colors['full_background'], 'padding': spaces['padding'], 'margin-top': '0px'})



if __name__ == '__main__':
    app.run_server(debug=True) 

