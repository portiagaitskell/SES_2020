import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, MATCH, ALL
import dash_bootstrap_components as dbc
import pandas as pd
import requests

from datetime import date, timedelta

# today = date.today()
#
# # Textual month, day and year
# d2 = today.strftime("%B %d, %Y")
# print("d2 =", d2)
#
# # mm/dd/y
# d3 = today.strftime("%m/%d/%y")
# print("d3 =", d3)
#
# # Month abbreviation, day and year
# d4 = today.strftime("%b-%d-%Y")
# print("d4 =", d4)
#
# slider_marks = {8-k: (today-timedelta(k)).strftime("%m/%d/%y") for k in range(8,-1,-1)}
#
# step=1
# slider_set = 8
#
# print(slider_marks)

API_KEY = 'ee193772a41f4eec96caa9325f6f9ab6'

# Import dataFrames if already saved
#df_1 = pd.read_csv('df_1.csv')
#df_2 = pd.read_csv('df_2.csv')
#df_3 = pd.read_csv('df_3.csv')


df_1 = None
df_2 = None
df_3 = None
dfs = [df_1, df_2, df_3]
index_conversion = {'entertainment':0, 'technology':1, 'sports':2}


# uncomment if dataframes not already saved
for i, category in enumerate(['entertainment','technology','sports']):
    dfs[i]= pd.DataFrame(columns=['source_id', 'source_name', 'title', 'description', 'url'])

    url = ('http://newsapi.org/v2/top-headlines?country=us&category={category}&apiKey={api}').format(api=API_KEY, category=category)

    response = (requests.get(url)).json()

    for article in response['articles']:
        vals = [article['source']['id'], article['source']['name'], article['title'], article['description'],
                article['url']]
        dfs[i] = dfs[i].append(pd.Series(vals, index=dfs[i].columns), ignore_index=True)


# Used to make keyword, and date searches
def search(keyword, start_date, end_date, API_KEY='ee193772a41f4eec96caa9325f6f9ab6'):
    url = 'https://newsapi.org/v2/everything?q={keyword}&from={start}&to={end}&sortBy=popularity&apiKey={API}'.format(keyword=keyword, API=API_KEY, start=start_date, end=end_date)
    response = (requests.get(url)).json()

    print(response)
    if response['status'] == 'error':
        return None

    else:
        df = pd.DataFrame(columns=['source_id', 'source_name', 'title', 'description', 'url', 'urlToImage'])

        for article in response['articles']:
            vals = [article['source']['id'], article['source']['name'], article['title'], article['description'],
                    article['url'], article['urlToImage']]
            df = df.append(pd.Series(vals, index=df.columns), ignore_index=True)

        return df


external_stylesheets = ['style.css',dbc.themes.CYBORG]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div(
    [
        html.Div(
            [
                html.H1("News App"),
                html.H6("Capital One SES Entry"),
                html.H6("By: Portia Gaitskell"),
            ]
        ),

        html.Div([
                html.Div([
                    html.H3('Category'),
                    dcc.Dropdown(id='type-selection',
                        options=[
                            {'label': 'Entertainment', 'value': 'entertainment'},
                            {'label': 'Technology', 'value': 'technology'},
                            {'label': 'Sports', 'value': 'sports'}
                        ],  optionHeight=65,
                        value='entertainment',
                    ),
                    html.Div([
                        html.H3('Keyword Search'),
                        dcc.Input(
                            id = 'search-keyword',
                            placeholder='Input a keyword...',
                            type='text',
                            value=''
                        ),
                        dcc.DatePickerRange(
                            #id = 'date-picker',
                            month_format='MMM Do, YY',
                            end_date_placeholder_text='MMM Do, YY',
                            start_date_placeholder_text='MMM Do, YY',
                            #start_date=date(2017,6,21)
                    id='calendar-container'),

                        dbc.Button("Search", id='search-button', className="ml-auto", n_clicks=0)
                    ], id="search-container"
                    )

                ],
                    className="dropdown column"),

                html.Div([
                    html.H3('Top Headlines', id='top-news-title'),
                    html.H5(children=["Loading articles..."], id="top-news-content")
                ],
                id="top-news-container", className="four columns"),

                html.Div([
                    html.H3('Searched Headlines'),
                    html.H5(children=['Loading...'], id='search-content')
                ], id='searched-container', className='four columns'
                ),


                html.Div(children=[], id='modal-container'),

                html.Div(children=[], id='modal-container2')

            ], className="data-container"),
    ],
    className="", id='main-container'
)


@app.callback(
    [Output('top-news-content', 'children'),
     Output('top-news-title', 'children'),
     Output('modal-container', 'children'),
     ],
    [Input('type-selection', 'value')])
def update_figure(article_type):
    print(article_type)

    title = 'Today\'s Top News Articles in {x}'.format(x=article_type.capitalize())

    df = dfs[index_conversion[article_type]]

    #info = df.iloc[0]
    #hret=c['url']
    # add a button
    # create a pattern matched button
    # give each button a id that's a dictionary
    html_lines = []
    modal_content = []
    for i, c in enumerate(df.iloc):
        #index = i+index_conversion[article_type]
        index = i
        #modal_type = 'modal-' + str(article_type)
        button_id = {'type': 'button-preview', 'index':index}
        modal_id = {'type': 'modal-popup', 'index': index}
        #modal_id = {'type': modal_type, 'index': index}
        close_id = {'type': 'modal-close', 'index': index}

        description = c['description']

        if isinstance(description, float):
            description = 'No preview available'

        line = html.Div([html.A(html.P(c['title']), href=c['url'], target='_blank'), html.Button('Preview', id=button_id, n_clicks=0)], id='article-container')
        html_lines.append(html.A(line))

        source = 'Source: ' + str(c['source_name'])

        modal = dbc.Modal([
                    dbc.ModalHeader(html.H1(c['title'])),
                    dbc.ModalBody([html.H3(description), html.H3(source)], id='modal-content'),
                    dbc.ModalFooter(children=[ html.A(html.H4('Link to article'), href=c['url'], target='_blank'),
                        dbc.Button("Close", id=close_id, className="ml-auto", n_clicks=0)
                    ]),
                ],
                id=modal_id,size="lg", is_open=False
            )
        #modal.
        modal_content.append(modal)


    article_html = html.Div(html_lines)
    #article_html = html.Div([html.A(html.P(c['title']), href=c['url'], target='_blank') for c in df.iloc],[])
    #article_html = html.Div([html.A(html.P(children=info['title']), id="preview-link")])

    return [article_html, title, modal_content]

@app.callback(
    Output({'type': 'modal-popup', 'index': MATCH}, 'is_open'),
    [Input({'type': 'button-preview', 'index': MATCH}, 'n_clicks'),
     Input({'type': 'modal-close', 'index': MATCH}, 'n_clicks')],
    [State({'type': 'button-preview', 'index': MATCH}, 'id'),
     State({'type': 'modal-popup', 'index': MATCH}, 'is_open')],
)
def display_output(n_preview, n_close, id, is_open):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if n_preview==0 and n_close == 0:
        return False

    change_dict = {}
    if len(changed_id) > 5:
        changed_id = changed_id.strip('.n_clicks')[1:-1]
        for elt in changed_id.split(","):
            line = elt.split(':')
            k = line[0].strip('\"')
            v = line[1].strip('\"')
            try:
                v = int(v)
            except:
                pass
            change_dict[k]=v

        button_type = change_dict['type']
        if button_type == 'modal-close':
            return False
        else:
            idx = change_dict['index']
            if idx == id['index']:
                return True
            elif idx != id['index'] and is_open:
                return False
            else:
                return False
    return False

@app.callback(
    [Output("search-content", "children"),
     Output('modal-container2', 'children')],
    [Input("search-button", "n_clicks")],
    [State('search-keyword', 'value'),
     State('calendar-container', 'start_date'),
     State('calendar-container', 'end_date')],
)
def update_output(n_click, keyword, start, end):

    #print(start)
    #print(end)

    #return 'Testing ' + str(keyword)
    #return u'Input 1 {} and Input 2 {}'.format(input1, input2)

    if n_click > 0 and len(keyword) > 0:
        df = search(keyword, start, end)

        if df is None:
            return ['Error Request. Please check that date entered is within 1 month of current date due to query limitations.', None]

        html_lines = []
        modal_content = []

        for i, c in enumerate(df.iloc):
            # index = i+index_conversion[article_type]
            index = i
            # modal_type = 'modal-' + str(article_type)
            button_id = {'type': 'search-button-preview', 'index': index}
            modal_id = {'type': 'search-modal-popup', 'index': index}
            close_id = {'type': 'search-modal-close', 'index': index}

            description = c['description']

            if isinstance(description, float):
                description = 'No preview available'

            line = html.Div([html.A(html.P(c['title']), href=c['url'], target='_blank'),
                             html.Button('Preview', id=button_id, n_clicks=0)], id='article-container')
            html_lines.append(html.A(line))

            source = 'Source: ' + str(c['source_name'])

            modal = dbc.Modal([
                dbc.ModalHeader(html.H1(c['title'])),
                dbc.ModalBody([html.H3(description), html.H3(source)], id='search-modal-content'),
                dbc.ModalFooter(children=[html.A(html.H4('Link to article'), href=c['url'], target='_blank'),
                                          dbc.Button("Close", id=close_id, className="ml-auto", n_clicks=0)
                                          ]),
            ],
                id=modal_id, size="lg", is_open=False
            )
            # modal.
            modal_content.append(modal)

        article_html = html.Div(html_lines)


        return [article_html, modal_content]

    return [None, None]


@app.callback(
    Output({'type': 'search-modal-popup', 'index': MATCH}, 'is_open'),
    [Input({'type': 'search-button-preview', 'index': MATCH}, 'n_clicks'),
     Input({'type': 'search-modal-close', 'index': MATCH}, 'n_clicks')],
    [State({'type': 'search-button-preview', 'index': MATCH}, 'id'),
     State({'type': 'search-modal-popup', 'index': MATCH}, 'is_open')],
)
def display_output(n_preview, n_close, id, is_open):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if n_preview==0 and n_close == 0:
        return False

    change_dict = {}
    if len(changed_id) > 5:
        changed_id = changed_id.strip('.n_clicks')[1:-1]
        for elt in changed_id.split(","):
            line = elt.split(':')
            k = line[0].strip('\"')
            v = line[1].strip('\"')
            try:
                v = int(v)
            except:
                pass
            change_dict[k]=v

        button_type = change_dict['type']
        print(button_type)
        if button_type == 'search-modal-close':
            return False
        else:
            idx = change_dict['index']
            if idx == id['index']:
                return True
            elif idx != id['index'] and is_open:
                return False
            else:
                return False
    return False






if __name__ == '__main__':
    app.run_server(debug=True)