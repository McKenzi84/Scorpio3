import dash 
import dash_bootstrap_components as dbc
from dash import html, dcc
import os

dash.register_page(__name__,path='/', order=1)

videos = [  "/assets/ScorpioLogo.mp4" ,
            "/assets/ace_logo_slate.mp4",
            ]

layout = dbc.Row([dbc.Col([
                    
            html.Br(),
            dcc.Markdown('Around Cutting Edge. \n '
            # ' Each page contains usefull informations regarding products manufacturing. \n '
            # ' If you have any requests or you find any bug please send info to: \n'
            ,
            style={'textAlign':'center', 'white-space': 'pre'}),
            html.Video(src=videos[0], autoPlay='autoPlay', muted='muted', width=800,style={'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto'}),  # Center video horizontally),
            #html.Video(src=video_url, autoPlay='autoPlay', loop='loop', muted='muted', width=800,style={'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto'})
            #carousel_items
],align='center') ], justify='center')  