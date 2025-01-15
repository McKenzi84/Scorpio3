import dash
from dash import Dash, Input, Output, State, callback, html
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify
import dash_bootstrap_components as dbc

import dash_mantine_components as dmc

from dash_auth import BasicAuth, add_public_routes

# dash._dash_renderer._set_react_version('18.2.0')


app = Dash(__name__,
            # external_stylesheets=dmc.styles.ALL,
            external_stylesheets=[dbc.themes.SLATE], #SLATE
            use_pages=True,
            prevent_initial_callbacks='initial_duplicate'
            )

server = app.server

def authorization_function(username, password):
    if (username == "hello") and (password == "world"):
        return True
    else:
        return False
    

BasicAuth(app, auth_func = authorization_function, secret_key="somestring")



def get_icon(icon):
    return DashIconify(icon=icon, height=16)

navbar = dbc.Navbar(
    
    dbc.Container(
        [   
            dbc.Row(
                [dbc.Col( 
                 
                 width="200px"),
                 
                 
                  ],  
                justify="center",  # Horizontal centering
                align="center",    # Vertical centering
                style={"height": "40px"},

                ),
         
                        
        ], fluid=True,
    ),
    #color="grey",
    className='top-navbar',
    sticky="top"
    # dark=True,
    
)

                       
                  

apps_pages = [dmc.NavLink( label= page["name"], href= page["path"] ) 
                for page in dash.page_registry.values() 
                if page["path"].startswith("/app") if page["module"] != "pages.not_found_404" ]


sidebar = html.Div(
    className="sidebar",
    style={"display": "flex", "flexDirection": "column", "height": "100vh"},  # ustawienie kolumny na pełną wysokość widoku
    children=[
        # Górna część z istniejącymi elementami
        html.Div(
            className="sidebar-content",
            style={"flexGrow": 1},  # zajmuje całą dostępną przestrzeń w górnej części
            children=[
                html.Div(

                        [html.A(
                            href="/",
                            children=[
                                html.Img(src='/assets/logo_ace.png',)
                            ]
                        )],
                     
                    className="sidebar-image", ),

                html.Hr(),
               
                dmc.NavLink(
                    label="Inne",
                    icon=get_icon(icon="flat-ui:settings"),
                    childrenOffset=28,
                    opened=False,
                    children=apps_pages),
            ],
        ),
        # Dolna część z nowym elementem wyrównanym do dołu
        html.Div(
            className="sidebar-footer",
            #style={"padding": "40px", "borderTop": "0px solid #ccc"},  # opcjonalne stylizacje
            children=[
                # html.Div("Nowy Element", style={"textAlign": "center"}),
                 html.Img(src='/assets/scorpio.svg',
                        # style={'width': '120px', 'height': '120px', 
                        #         #   'filter': 'invert(0.5) sepia(1) saturate(10) hue-rotate(180deg)'
                        #           'filter': 'invert(1) brightness(2)'
                        #           ,},
                        className='sidebar_svg',
                                  )  # adjust as needed
            ],
        ),
    ],
)


app.layout = dmc.MantineProvider(
    [   
        navbar,
        sidebar,
        html.Div([dash.page_container,], className="content" ),
    ]
)


if __name__ == "__main__":
    app.run_server() 