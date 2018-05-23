import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd

import io
import base64

app = dash.Dash()

app.scripts.config.serve_locally = True
app.config['suppress_callback_exceptions'] = True

app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-data-upload'),
    html.Div(id='graph')
])
def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    global file_name 
    file_name = filename
    try:
        if 'csv' in filename:
            global df
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            column = list(df)
        elif 'xls' in filename:
            df = pd.read_excel(io.BytesIO(decoded))
            column = list(df)
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.Div([
        html.Div([
        html.Div('Select X-Axis:'),
        dcc.Dropdown(
            id='xaxis',
            options = [ {'label': i, 'value': i} for i in column],
        ),
        ],
        style={'width': '35%', 'display': 'inline-block'}),

        html.Div([
        html.Div('Select Y-Axis:'),
        dcc.Dropdown(
            id='yaxis',
            options = [ {'label': i, 'value': i} for i in column],
        ),
        ],
        style={'width': '35%', 'display': 'inline-block'}),

        html.Div([
        html.Div('Select Graph Type:'),
        dcc.Dropdown(
            id='type',
            options = [{'label': 'line', 'value': 'line'},
                       {'label': 'bar', 'value': 'bar'}],
            value='line'
        ),
        ],
        style={'width': '30%', 'display': 'inline-block'}),
        ]),
    ])


@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents'),
               Input('upload-data', 'filename'),
               Input('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children


@app.callback(
    Output('graph', 'children'),
    [Input('xaxis', 'value'),
     Input('yaxis','value'),
     Input('type','value')])
def update_graph(xaxis, yaxis, type):
    return dcc.Graph(
        id='graph_bddata',
        figure={
            'data':[
                {'x':list(df[xaxis]),'y':list(df[yaxis]),'type':type,'name':'Population'},
            ],
            'layout':{
                'title':file_name,
            },
        }
    )

app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

if __name__ == '__main__':
    app.run_server(debug=True)