import requests
import pandas as pd
#
# API_KEY = '07030a5437224023b9c9bd4148da4541'
#
# #URL = 'ttps://www.ft.com/content/bef48683-9bde-4ac2-8906-797779593b22'
# #r = requests.get(url = URL)
#
# #print(r.json() )
#
# url = ('http://newsapi.org/v2/top-headlines?'
#        'country=us&'
#        'apiKey={api}').format(api=API_KEY)
#
# #print(url)
#
# #response = requests.get(url)
# #print(response.json())
#
# url2 = ('http://newsapi.org/v2/top-headlines?'
#        'sources={source}&'
#        'apiKey={api}').format(api=API_KEY, source='')
#
# url3 = ('https://newsapi.org/v2/sources?apiKey=07030a5437224023b9c9bd4148da4541')
#
#
# response3 = requests.get(url3)
# print(response3.json())
#
#
# categories = ['entertainment', 'sports', 'technology']
# url4 = 'http://newsapi.org/v2/top-headlines?country=us&category={category}&apiKey=07030a5437224023b9c9bd4148da4541'.format(category=categories[0])
#
# response4 = requests.get(url4)
# print(response4.json())
#
#
# url5 = 'https://newsapi.org/v2/everything?q=bitcoin&apiKey=07030a5437224023b9c9bd4148da4541'
#
# response5 = requests.get(url5)
#
# print(response5.json())

def search(keyword, start_date, end_date, API_KEY='ee193772a41f4eec96caa9325f6f9ab6'):
    url = 'https://newsapi.org/v2/everything?q={keyword}&from={start}&to={end}&sortBy=popularity&apiKey={API}'.format(keyword=keyword, API=API_KEY, start=start_date, end=end_date)
    #url='https://newsapi.org/v2/everything?q=bitcoin&apiKey={API}'.format(API=API_KEY)
    response = (requests.get(url)).json()

    df = pd.DataFrame(columns=['source_id', 'source_name', 'title', 'description', 'url', 'urlToImage'])

    for article in response['articles']:
        vals = [article['source']['id'], article['source']['name'], article['title'], article['description'],
                article['url'], article['urlToImage']]
        df = df.append(pd.Series(vals, index=df.columns), ignore_index=True)

    return df


# print(search('bitcoin', '2020-11-01', '2020-11-04'))
