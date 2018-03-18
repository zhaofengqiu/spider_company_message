import requests
from lxml import etree
from bs4 import BeautifulSoup
import time
import re,random
from project import app
from exts import db
from models import New,Article
db.init_app(app)
def insertuser(url,headline,summary):
    with app.app_context():
        try:
            new = New(url=url, headline=headline, summary=summary)
            db.session.add(new)
            db.session.commit()
            new = New.query.filter(New.url == url).first()
        except Exception as ce:
            print(ce)
    return new
def insertarticle(datetime,new_id,section,text):
    with app.app_context():
        try:
            article = Article(section=section,text=text,datetime=datetime,article_id=new_id)
            db.session.add(article)
            db.session.commit()
            print('succeed')
            time.sleep(2)
        except Exception as ce:
            print(ce)
header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
def getdetail(url,new_id,section):
    text=''
    r=requests.get(url)
    data=etree.HTML(r.text)
    htmldata=BeautifulSoup(r.text,'html.parser')
    #new_texts=data.xpath('//p[@class="story-body-text story-content"]/text()')
    try:
        new_texts=htmldata.find_all('p',attrs={'class':'story-body-text story-content'})
        for new in new_texts:
            text=str(new)+text
        datetime =data.xpath('//*[@datetime]/@datetime')[0]
        time = datetime[::-1]
        time = time.split('-', maxsplit=1)[-1]
        datetime = time[::-1]
        insertarticle(datetime,new_id,section,text)
    except:
        pass
def getnews(url,section):
    global i, temple
    data=requests.get(url).text
    page_data = BeautifulSoup(data, 'html.parser')
    datas = page_data.find_all('div', attrs={'class': 'story-body'})
    for data in datas:
        headline = ''
        picture_url = data.find_all(attrs={'href': True})[0].get('href')
        headlines = data.find_all(attrs={'class': 'headline'})[0].strings
        for text in headlines:
            headline = headline + text
        summary = data.find_all(attrs={'class': 'summary'})[0].string
        new=insertuser(url,headline,summary)
        if new.id:
            getdetail(picture_url, section, new.id)
def getindex(url):
    htmldata = requests.get(url).text
    data = BeautifulSoup(htmldata, 'html.parser').find(id="top-news")
    newsdata = data.find_all('article', attrs={'class': 'story'})
    for newdata in newsdata:
        headline = ''
        summary = ''
        try:
            url = newdata.find('a')['href']
            headlinedata = newdata.find(attrs={'class': 'story-heading'}).strings
            for string in headlinedata:
                headline = string + headline
            summarydata = newdata.find(attrs={'class': 'summary'}).strings
            for string in summarydata:
                summary = string + summary
        except Exception as ce:
            summary = 'none'
        new=insertuser(url,headline,summary)
        if new.id:
            getdetail(url,new.id,section='Top_new')
    list = re.findall('(<li class="shortcuts-.*?</li>)', htmldata, re.S)
    for lis in list:
        li = BeautifulSoup(lis, 'html.parser')
        url = li.a.get('href')
        section = li.a.string
        print(url, section)
        getnews(url, section)
if __name__ == '__main__':
    url="https://www.nytimes.com/"
    getindex(url)

"""
外键一定是intl类型，我们可以在new里面找到id复制到article里面的id
"""