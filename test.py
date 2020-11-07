# import requests
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

changed_id = '{"index":0,"type":"button-preview"}.n_clicks'
changed_id = changed_id.replace('.n_clicks',"")[1:-1]
change_dict = {}
print(changed_id)
for elt in changed_id.split(","):
       line = elt.split(':')
       k = line[0].strip('\"')
       v = line[1].strip('\"')
       change_dict[k]=v
print(change_dict)

