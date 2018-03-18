
DEBUG = True
HOSTNAME=''#数据库所在的服务器ip
PORT    ='3306'
DATABASE=''#数据库名
USERNAME=''#数据库用户名
PASSWORD=''#密码
SQLALCHEMY_TRACK_MODIFICATIONS=False
DB_URI  ='mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,PASSWORD,
        HOSTNAME,PORT,DATABASE)
SQLALCHEMY_DATABASE_URI=DB_URI
