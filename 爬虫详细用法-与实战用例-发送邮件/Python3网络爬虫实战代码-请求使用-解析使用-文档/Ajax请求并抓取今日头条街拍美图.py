import re
import requests
import json
from urllib.parse import urlencode
from requests.exceptions import RequestException
from bs4 import BeautifulSoup

def get_page_index(offset,keyword):
    data = {
        'offset':keyword,
        'format':'json',
        'keyword':keyword,
        'autoload':'true',
        'count':20,
        'cur_tab':1,
        'from':'search_tab'
    }
    url = 'https://www.toutiao.com/search_content/?'+ urlencode(data)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求失败')
        return None

def parse_page_index(html):
    data = json.loads(html)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            yield item.get('article_url')

def get_page_detail(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求详情页出错',url)


def parse_page_detail(html,url):
    so = BeautifulSoup(html,'lxml')
    title = so.select('title')[0].get_text
    images_pattern = re.compile('var gallery = (.*?);',re.S)
    result = re.search(images_pattern,html)
    if result:
        data = json.load(result.group(1))
        if data and 'sub_images' in data.keys():
            sub_images = data.get('sub_imges')
            images = [item.get('url')for item in sub_images]
            return{
                'title':title,
                'url':url,
                'images':images
            }
def main():
    html = get_page_detail(0,'街拍')
    for url in parse_page_index(html):
        html = get_page_detail(url)
        if html:
           result = parse_page_detail(html,url)
           print(result)

if __name__=='__main__':
    main()