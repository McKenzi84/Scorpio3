import dash 
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Output, Input, State, clientside_callback
import pandas as pd
import pymupdf
import io
import base64
from dash.exceptions import PreventUpdate
import base64
from datetime import datetime

dash.register_page(__name__, name='1. MPS1 - rysunki ',)

border = {  'border': '1px outset black',  'border-radius': '5px'}

df = pd.read_excel('mps1_drawing/mps1_all.xlsx')


def mps1_manual(tool_diameter):
    match tool_diameter:
        case d if d == 3:
            v_part = '0.05~0.11'
            x_part = '0.08~0.12'
            w1 = '0.03~0.055'
            w2 = '0.03x45°'
            
        case d if 3 < d <= 8:
            v_part = '0.07~0.13'
            x_part = '0.13~0.17'
            w1 = '0.04~0.07'
            w2 = '0.04x45°'
            
        case d if 8 < d <= 12:
            v_part = '0.15~0.21'
            x_part = '0.20~0.24'
            w1 = '0.07~0.12'
            w2 = '0.06x45°'

        case d if 12 < d <= 14:
            v_part = '0.25~0.35'
            x_part = '0.30~0.34'
            w1 = '0.12~0.17'
            w2 = '0.11x45°'

        case _:
            v_part = 'Tool diameter not in range'
            x_part = 'Tool diameter not in range'
            w1 = 'Tool diameter not in range'
            w2 = 'Tool diameter not in range'
            #return "Tool diameter not in range"
    
    # print(f'Tool diameter: {tool_diameter}')
    # print(f'V_part:{v_part}')
    # print(f'X_part:{x_part}')
    # print(f'W1:{w1}')
    # print(f'W2:{w2}')

    return(v_part, x_part, w1, w2)




layout = html.Div([
            dbc.Row(children=[
                html.Br(),
                html.Br(),
                html.P('Generowanie rysunku ostrzarskiego dla MPS1'),
                html.Div(id = 'selected_mps1'),
                dcc.Store(id='mps1_store'), 

            ], 
            style={ 'text-align': 'center','border': '1px outset black',  'border-radius': '5px'}), #'background-color': 'white',
            
            dbc.Row(children=[
                dbc.Col(children=[
                    dbc.InputGroup([dbc.InputGroupText("Średnica"), dbc.Input(id='mps1_tool_dia', type='number')],size='sm'),
                    html.Br(), 
                    dcc.Dropdown(id='mps1_dropdown',
                             #options=[{'label': f'{x}', 'value': (x)} for x in ['LEWY', 'PRAWY']],
                             style={'color':'black', 'width': '100%'},placeholder="", value=''),

                    html.Br(),
                    html.Br(), 
                    # dbc.InputGroup([dbc.InputGroupText("Tool no."), dbc.Input(id='tool_no')],size='sm'),
                    # dbc.InputGroup([dbc.InputGroupText("Drawing no: "), dbc.Input(id='drawing_no',)],size='sm'),
                    dbc.Button('Podgląd rysunku', id='mps1_pdf_preview', style={'width':'80%', }),

                    

                ], width=2, 
                             style={
                                'display': 'flex',          # Flexbox layout
                                'flexDirection': 'column',  # Ustawienie elementów w kolumnie
                                'alignItems': 'center', 
                                'border': '1px outset black',  'border-radius': '5px'    # Wyrównanie elementów w poziomie
                                # 'justifyContent': 'center', # Opcjonalnie: wyśrodkowanie w pionie
                                # 'height': '100vh'           # Opcjonalnie: wysokość kontenera na całą stronę
                                } 
            ), #style={'background-color': 'blue'}


                dbc.Col(children=[
                                dcc.Loading(
                                html.ObjectEl(
                                id = 'pdf_preview',
                                #data= '/mps1_drawing_template.pdf', #assets\sample_report.pdf
                                type="application/pdf",
                                style={"width": "100%", "height": "700px",},
                                ),),

                                dbc.Button('Pobierz rysunek', id='mps1_pdf_download', style={'width':'80%', }),
                                html.Div(id="placeholder")
                ], width=10 , 
                style={
                                'display': 'flex',          # Flexbox layout
                                'flexDirection': 'column',  # Ustawienie elementów w kolumnie
                                'border': '1px outset black',  'border-radius': '5px'

                } )
            ])
])

######## Choose MPS
@callback(
            Output('mps1_dropdown', 'options'),
            Input('mps1_tool_dia', 'value'),
            prevent_initial_call=True          
)

def mps1_options_drop(tool_dia):

    df['DC'] = pd.to_numeric(df['DC'], errors='coerce')
    result = df.loc[df['DC'] == tool_dia, 'Text'].tolist()

    return result


#############################
@callback(
            Output('mps1_store', 'data'),
            Output('selected_mps1', 'children'), # Set for file  name during download
            Input('mps1_pdf_preview', 'n_clicks'),
            State('mps1_dropdown', 'value'),
            prevent_initial_call=True          
)

def store_pdf_content(n_clicks, mps1_selected):
    #print(contents)
    if n_clicks:

        try:
            
            template_file = 'mps1_drawing/MPS1_TEMPLATE.pdf' # 297x210 / A4 Horizontal / Template prepared in Zuou. 
            pdf_sp = pymupdf.open(template_file)
            page1 = pdf_sp.load_page(0)
            page1_width = page1.rect.width # X
            page1_height = page1.rect.height # Ypa

            sample_mps_dimensions =  df[df['Text'] == mps1_selected].to_dict(orient='records')

            v_part, x_part, w1, w2 = mps1_manual(float(sample_mps_dimensions[0]['DC']))

            today = datetime.today()
            drawing_degenration_date = today.strftime('%d-%m-%Y')

            table_items =  [
                            {'point': pymupdf.Point(page1_width/297 * 172 ,page1_height/210 * 90.5) ,'angle': 0, 'text' : f"ø{str(sample_mps_dimensions[0]['DC'])}", "fontsize" : 10, },

                            {'point': pymupdf.Point(page1_width/297 * 181.9 ,page1_height/210 * 88.5) ,'angle': 0, 'text' : f"{str(sample_mps_dimensions[0]['Tolerancja maks. średnicy krawędzi skrawającej'])}", "fontsize" : 8, },
                            {'point': pymupdf.Point(page1_width/297 * 181 ,page1_height/210 * 91.5) ,'angle': 0, 'text' : f"{str(sample_mps_dimensions[0]['Tolerancja min. średnicy krawędzi skrawającej'])}", "fontsize" : 8, },

                            {'point': pymupdf.Point(page1_width/297 * 173 ,page1_height/210 * 98) ,'angle': 0, 'text' : f"ø{str(sample_mps_dimensions[0]['DCON'])} h6", "fontsize" : 10, },
                            {'point': pymupdf.Point(page1_width/297 * 173 ,page1_height/210 * 106) ,'angle': 0, 'text' : f"{str(sample_mps_dimensions[0]['OAL'])}", "fontsize" : 10, },
                            {'point': pymupdf.Point(page1_width/297 * 173 ,page1_height/210 * 114) , 'angle': 0,'text' : f"{str(sample_mps_dimensions[0]['SIG'])}" , "fontsize" : 10,},
                            {'point': pymupdf.Point(page1_width/297 * 173 ,page1_height/210 * 122) ,'angle': 0, 'text' : f"6°~8°", "fontsize" : 10, },
                            {'point': pymupdf.Point(page1_width/297 * 173 ,page1_height/210 * 130) , 'angle': 0,'text' : f" 25°" , "fontsize" : 10,},
                            {'point': pymupdf.Point(page1_width/297 * 171 ,page1_height/210 * 138) , 'angle': 0,'text' : f"{x_part}" , "fontsize" : 10,},
                            {'point': pymupdf.Point(page1_width/297 * 171 ,page1_height/210 * 146) , 'angle': 0,'text' : f"{w1}" , "fontsize" : 10,},
                            {'point': pymupdf.Point(page1_width/297 * 173 ,page1_height/210 * 153) , 'angle': 0,'text' : f"0.02", "fontsize" : 10, },
                            {'point': pymupdf.Point(page1_width/297 * 150 ,page1_height/210 * 10) , 'angle': 0, 'text' : f" {mps1_selected}" , "fontsize" : 12,},

                            {'point': pymupdf.Point(page1_width/297 * 75 ,page1_height/210 * 12) , 'angle': 0,'text' : f"{v_part}" , "fontsize" : 12,},
                            {'point': pymupdf.Point(page1_width/297 * 75 ,page1_height/210 * 50) , 'angle': 0,'text' : f"{x_part}" , "fontsize" : 12,},
                            {'point': pymupdf.Point(page1_width/297 * 75 ,page1_height/210 * 97) , 'angle': 0,'text' : f"{w1}" , "fontsize" : 12,},
                            {'point': pymupdf.Point(page1_width/297 * 75 ,page1_height/210 * 140) , 'angle': 0,'text' : f"{w2}" , "fontsize" : 12,},

                            {'point': pymupdf.Point(page1_width/297 * 278.5 ,page1_height/210 * 203) , 'angle': 0,'text' : f"{drawing_degenration_date}" , "fontsize" : 8,},
                        

                            # {'point': pymupdf.Point(page1_width/297 * 85 ,page1_height/210 * 25.5) , 'angle': 0,'text' : f"{str(sample_mps_dimensions[0]['LF'])}" },
                            # # {'point': pymupdf.Point(page1_width/297 * 30 ,page1_height/210 * 25.5) , 'text' : f"{str(sample_mps_dimensions[0]['PL'])}" }, # This value is not present in the list.
                            # {'point': pymupdf.Point(page1_width/297 * 77 ,page1_height/210 * 75.6) ,'angle': 0, 'text' : f"{str(sample_mps_dimensions[0]['OAL'])}" },
                            # {'point': pymupdf.Point(page1_width/297 * 62.5 ,page1_height/210 * 70.5) ,'angle': 0, 'text' : f"{str(sample_mps_dimensions[0]['LH'])}" },
                            # {'point': pymupdf.Point(page1_width/297 * 112 ,page1_height/210 * 71) ,'angle': 0, 'text' : f"{str(sample_mps_dimensions[0]['LS'])}" },
                            # {'point': pymupdf.Point(page1_width/297 * 66 ,page1_height/210 * 66) , 'angle': 0,'text' : f"{str(sample_mps_dimensions[0]['LCF'])}" },
                            # {'point': pymupdf.Point(page1_width/297 * 45 ,page1_height/210 * 60) , 'angle': 0,'text' : f"{str(sample_mps_dimensions[0]['SIG'])}" },

                            # {'point': pymupdf.Point(page1_width/297 * 34 ,page1_height/210 * 95) , 'angle': 0, 'text' : f"{ round(float(sample_mps_dimensions[0]['DC']) * 0.1 ,2)}" }
                            ]

            
            for item in table_items: 
                page1.insert_text(item['point'],  # bottom-left of 1st char
                                        item['text'],  # the text (honors '\n')
                                        fontname = "helv",  # the default font
                                        fontsize = item['fontsize'],  # the default font size
                                        rotate = item['angle'],  # also available: 90, 180, 270
                                        color = [1,0,0],
                                    )





            pdf_buffer = io.BytesIO()
            pdf_sp.save(pdf_buffer)
            pdf_sp.close()


            pdf_buffer.seek(0)  # Move to the beginning of the buffer
            encoded_pdf = base64.b64encode(pdf_buffer.read()).decode('utf-8')

            # pdf_sp.save('mps_preview.pdf')
            # with open('mps_preview.pdf', mode= 'rb',) as file: #encoding='cp932', errors='ignore'
            #     encoded_pdf = base64.b64encode(file.read()).decode('utf-8')
            #     print(encoded_pdf)
            return f'data:application/pdf;base64,{encoded_pdf}'  , mps1_selected    

        except Exception as e:
            print(e)
            # with open('genius_report/reports/sample_report.pdf', 'r') as file:
            #     data = file.read()
            return '', ""



########################################
@callback(Output('pdf_preview', 'data'),
        Input('mps1_store', 'data'),
        prevent_initial_call=True

        )


def pdf_preview(data):
    if data is not None:
        return data
    
    # else: 
    #     with open('genius_report/sample_report.pdf', 'r') as file:
    #         data = file.read()
    #     return data    


    return "No PDF content to display." 
####################################
# Add the JavaScript clientside callback
clientside_callback(
    """
    function(n_clicks, pdf_data, dropdown_value) {
        if (!n_clicks || !pdf_data) {
            return;
        }
        
        // Extract base64 data (remove the data:application/pdf;base64, prefix)
        const base64String = pdf_data.split(',')[1];
        
        // Convert base64 to binary
        const binaryString = atob(base64String);
        const len = binaryString.length;
        const bytes = new Uint8Array(len);
        for (let i = 0; i < len; i++) {
            bytes[i] = binaryString.charCodeAt(i);
        }
        
        // Create a Blob with PDF content
        const blob = new Blob([bytes], { type: 'application/pdf' });
        
        // Create a link element
        const link = document.createElement('a');
        link.href = window.URL.createObjectURL(blob);
		
		// Set the download filename based on dropdown value
        const filename = dropdown_value + '.pdf';
        link.download = filename;  // Use the dropdown value for the file name
        
        // Trigger the download
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        return null;  // No output for Dash
    }
    """,
    Output("placeholder", "children"),  # Placeholder output
    Input("mps1_pdf_download", "n_clicks"),  # Trigger on button click
    State("mps1_store", "data"),  # Get the stored PDF data
	State("selected_mps1", "children")  # Get the selected value from the dropdown
)