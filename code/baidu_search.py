import requests
import re

url = 'https://www.baidu.com/s'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36'}
r = re.compile('<h3[\s\S]*?<a[^>]*?href[^>]*?"(.*?)"[^>]*?>(.*?)</a >')

def baidu_search(keyword):
    params = {'wd': keyword, 'pn': 0, 'ie': 'utf-8'}
    try:
        response = requests.get(url, params, headers=headers)
        response.raise_for_status()
        content = response.content
        print(content) 
        for i in r.findall(content):
            yield (re.compile('<.*?>').sub('', i[1]).decode('utf8'), i[0])
        params['pn'] += 10
    except requests.RequestException as e:
        print(f"请求错误: {e}")
        while 1: yield ('', '')
    except Exception as e:
        print(f"其他错误: {e}")
        while 1: yield ('', '')
