import requests

from bili import headers


headers = headers.get('cookies.txt')
url = 'https://api.bilibili.com/x/v2/history?pn=1&ps=100&jsonp=jsonp'
resp = requests.get(url, headers=headers)
print(resp.text)