
"""
如何通过atticle访问user里面的元素?
首先设置外键和relation的正向访问和反向访问。
其次正向访问：
data.new.XXX
反向访问:

如果是app启动了的话，就会被自动推到栈顶。
"""
from flask import Flask,render_template,url_for,redirect
import config
app = Flask(__name__)
app.config.from_object(config)
from exts import db
from models import Article,New
db.init_app(app)
@app.route('/')
def hello_world():
    return redirect('/index/')

@app.route('/index/')
def index():
    datas = Article.query.filter(Article.section == 'Top_new').all()
    datas = sorted(datas, key=lambda article: article.datetime, reverse=True)
    data = {'kind': 'Top_new',
            'dat': datas}
    return render_template('section.html', new_data=data)

@app.route('/section/<sort>')
def section(sort):
    datas = Article.query.filter(Article.section == sort).all()
    datas=sorted(datas,key=lambda article :article.datetime,reverse=True)
    data={'kind':sort,
          'dat':datas}
    return render_template('section.html',new_data=data)

@app.route('/detail/<article_id>')
def detail(article_id):
    article=Article.query.filter(Article.id == article_id).first()

    return render_template('detail.html',articledata=article)
if __name__ == '__main__':
    app.run()

