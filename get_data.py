import pandas as pd
import requests

from datetime import date, timedelta

API_KEY = 'ee193772a41f4eec96caa9325f6f9ab6'

df_1, df_2, df_3 = None, None, None

dfs = [df_1, df_2, df_2]
index_conversion = {'entertainment':0, 'technology':1, 'sports':2}

for i, category in enumerate(['entertainment','technology','sports']):
    dfs[i]= pd.DataFrame(columns=['source_id', 'source_name', 'title', 'description', 'content', 'url', 'urlToImage', 'publishedAt'])

    url = ('http://newsapi.org/v2/top-headlines?country=us&category={category}&apiKey={api}').format(api=API_KEY, category=category)

    response = (requests.get(url)).json()

    for article in response['articles']:
        vals = [article['source']['id'], article['source']['name'], article['title'], article['description'], article['content'],
             article['url'], article['urlToImage'], article['publishedAt']]
        dfs[i] = dfs[i].append(pd.Series(vals, index=dfs[i].columns), ignore_index=True)


dfs[0].to_csv('df_1.csv')
dfs[1].to_csv('df_2.csv')
dfs[2].to_csv('df_3.csv')