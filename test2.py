import requests
import pandas as pd

API_KEY = '07030a5437224023b9c9bd4148da4541'

category='sports'

#url = 'https://newsapi.org/v2/everything?q=sports&from=2020-11-05&to=2020-11-05&sortBy=popularity&apiKey=07030a5437224023b9c9bd4148da4541'.format(category='sports')
#url = ('http://newsapi.org/v2/top-headlines?country=us&category={category}&apiKey={api}').format(api=API_KEY,
#                                                                                                 category=category)

# url = 'https://newsapi.org/v2/sources?apiKey=07030a5437224023b9c9bd4148da4541'
# response = (requests.get(url)).json()
# print(response)


# category = 'sports'
# url = ('http://newsapi.org/v2/top-headlines?country=us&category={category}&apiKey={api}').format(api=API_KEY,
#                                                                                                  category=category)
#
# response = (requests.get(url)).json()
#
#
#     for article in response['articles']:
#         vals = [article['source']['id'], article['source']['name'], article['title'], article['description'],
#                 article['url']]
#         dfs[i] = dfs[i].append(pd.Series(vals, index=dfs[i].columns), ignore_index=True)
#
# print(len(dfs))
# count = 0
# for elt in dfs:
#     print(count)
#     count+=1
#     print(elt)