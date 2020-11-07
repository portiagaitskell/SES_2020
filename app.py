import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, MATCH, ALL
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import requests

from datetime import date, timedelta

today = date.today()

# Textual month, day and year
d2 = today.strftime("%B %d, %Y")
print("d2 =", d2)

# mm/dd/y
d3 = today.strftime("%m/%d/%y")
print("d3 =", d3)

# Month abbreviation, day and year
d4 = today.strftime("%b-%d-%Y")
print("d4 =", d4)

slider_marks = {8-k: (today-timedelta(k)).strftime("%m/%d/%y") for k in range(8,-1,-1)}

step=1
slider_set = 8

print(slider_marks)

API_KEY = 'ee193772a41f4eec96caa9325f6f9ab6'
df_1 = pd.read_csv('df_1.csv')
df_2 = pd.read_csv('df_2.csv')
df_3 = pd.read_csv('df_3.csv')

index_start = {'entertainment':0, 'technology':len(df_1), 'sports':len(df_1)+len(df_2)}

dfs = [df_1, df_2, df_2]
index_conversion = {'entertainment':0, 'technology':1, 'sports':2}

# for i, category in enumerate(['entertainment','technology','sports']):
#     dfs[i]= pd.DataFrame(columns=['source_id', 'source_name', 'title', 'description', 'url'])
#
#     url = ('http://newsapi.org/v2/top-headlines?country=us&category={category}&apiKey={api}').format(api=API_KEY, category=category)
#
#     response = (requests.get(url)).json()
#
#     for article in response['articles']:
#         vals = [article['source']['id'], article['source']['name'], article['title'], article['description'],
#                 article['url']]
#         dfs[i] = dfs[i].append(pd.Series(vals, index=dfs[i].columns), ignore_index=True)

#df_1 = pd.read_csv('df_1.csv')
#df_2 = pd.read_csv('df_2.csv')
#df_3 = pd.read_csv('df_3.csv')

#dfs = [df_1, df_2, df_3]

external_stylesheets = ['style.css',dbc.themes.CYBORG]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div(
    [
        html.Div(
            [
                html.H1("Title"),
                html.H6("Capital One SES Entry: Portia Gaitskell"),
            ]
        ),

        # html.Div(
        #         [
        #             dcc.Slider(
        #                 id='slider',
        #                 min=min(slider_marks),
        #                 max=max(slider_marks),
        #                 step=step,
        #                 marks=slider_marks,
        #                 value=slider_set
        #             ),
        #         ]
        #     ),

        html.Div([
                html.Div([
                    html.H3('Dropdown'),
                    dcc.Dropdown(id='type-selection',
                        options=[
                            {'label': 'Entertainment', 'value': 'entertainment'},
                            {'label': 'Technology', 'value': 'technology'},
                            {'label': 'Sports', 'value': 'sports'}
                        ],
                        value='entertainment',
                    ),
                ], className="dropdown column"),

                html.Div([
                    html.H3('Top Headlines', id='top-news-title'),
                    html.H5(children=["Loading articles..."], id="top-news-content")
                ],
                id="top-news-container", className="five columns"),

                html.Div(children=[], id='modal-container')


            #     dbc.Modal([
            #         dbc.ModalHeader("Header"),
            #         dbc.ModalBody(children=[], id='modal-content'),
            #         dbc.ModalFooter(
            #             dbc.Button("Close", id="close", className="ml-auto")
            #         ),
            #     ],
            #     id="modal",
            # ),

                # html.Div([
                #     html.H3('Article Preview'),
                #     html.H5([html.P(children=['loading preview'], id='preview-link')], id="preview-content")
                # ],
                # id="preview-container", className="five columns"),
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

        modal = dbc.Modal([
                    dbc.ModalHeader(html.H1(c['title'])),
                    dbc.ModalBody(html.H3(description), id='modal-content'),
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
    print('XX')
    print('Preview:', n_preview)
    print(n_close)
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    print(changed_id)

    if n_preview==0 and n_close == 0:
        return False

    change_dict = {}
    if len(changed_id) > 5:
        changed_id = changed_id.strip('.n_clicks')[1:-1]
        #changed_id = changed_id[1:-1]
        print(changed_id)
        for elt in changed_id.split(","):
            line = elt.split(':')
            k = line[0].strip('\"')
            v = line[1].strip('\"')
            #print(int(v))
            try:
                v = int(v)
            except:
                pass
            change_dict[k]=v

        print(change_dict)
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


# @app.callback(
#     [Output("modal", "is_open"),
#      Output('modal-content', 'children')],
#     [Input({'type': 'button-preview', 'index': ALL}, 'n_clicks'),
#      Input("close", "n_clicks")],
#     [State({'type': 'button-preview', 'index': ALL}, 'id'),
#      State('type-selection', 'value'),
#      State('modal', 'is_open')],
# )
# def display_modal(n_clicks, close_button, id_val, article_type, is_open):
#     changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
#     print(changed_id)
#     changed_id = changed_id.replace('.n_clicks',"")[1:-1]
#     change_dict = {}
#     print(changed_id)
#
#     for elt in changed_id.split(","):
#         line = elt.split(':')
#         k = line[0].strip('\"')
#         v = line[1].strip('\"')
#         change_dict[k]=v
#
#     print(change_dict)
#     idx = change_dict['index']
#     print(idx)
#     #print(idx)
#     print(n_clicks)
#     #print(close_button)
#     #print(id_val)
#     #print(article_type)
#     #print(is_open)
#     if close_button and is_open:
#         return False, None
#
#     if is_open is False:
#         df = dfs[index_conversion[article_type]]
#         #idx = n_clicks.index(max(n_clicks))
#
#         #print(int(id_val['index']))
#         info = df.iloc[idx]
#         content = info['title']
#
#         return True, content
#
#     return False, None


# @app.callback(
#     [Output('preview-content', 'children'),
#      ],
#     [Input('preview-link', 'n-clicks'),
#      Input('preview-link', 'children'),
#      Input('type-selection', 'value')])
# def update_preview(n, title, article_type):
#     df = dfs[index_conversion[article_type]]
#     idx = df[df['title']==title].index.tolist()[0]
#
#     info = df.iloc[idx]
#     preview_html = html.Div([html.P(children=info['description'])])
#
#     return preview_html


if __name__ == '__main__':
    app.run_server(debug=True)