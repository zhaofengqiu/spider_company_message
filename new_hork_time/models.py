from exts import db
class New(db.Model):
    __tablename__='new'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    url= db.Column(db.String(400),nullable=False)
    headline= db.Column(db.String(400),nullable=False)
    summary = db.Column(db.Text, nullable=False)
class Article(db.Model):
    __tablename__='article'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    section=db.Column(db.String(400),nullable=False)
    text=db.Column(db.Text,nullable=False)
    datetime=db.Column(db.String(50),nullable=False)
    article_id=db.Column(db.Integer,db.ForeignKey('new.id'),nullable=False)
    new=db.relation('New',backref=db.backref('articles'))

