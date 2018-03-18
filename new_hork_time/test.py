from flask import Flask,render_template,url_for
from exts  import  db
from project import app
from models import New,Article
db.init_app(app)
from models import Article,New
import requests
url='https://www.nytimes.com/'
r=requests.get(url)
from bs4 import BeautifulSoup

    print('___________________________________________________')



