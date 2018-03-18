import re
import pymysql
import requests
from bs4 import BeautifulSoup

#下面是发送邮件的库
import smtplib
from email.mime.text import MIMEText
from email.header import Header


urlbanner = []
url="https:"
# 创建连接
conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='email',charset="utf8")
# 创建游标
cursor = conn.cursor()


#这个是登录的
def login():
    data = {
        "username":"",
        "password":"",
        "t":"validate"
    }

    url = ""
    s = requests.session()
    response = s.post(url,data=data)
    return s

def get_html(s):
    #这里重新请求第一个页面
    response = s.get("")
    if response.status_code==200:
        url_list=[]
        pattern = '<a target="_blank" href="(.*?banners_id=(\d+).*)">\s+<img'
        result = re.compile(pattern).findall(response.text)

        for i in result:
            #i[0],i[1],这里的写法是取上面两个括号中的数据，第一个取的是外层，第二个是内层
            #这是把url 和 id 传给get_detail方法
            get_detail(s, url + i[0],i[1])
    else:
        print("Wrong")

#获取banner行数的总数
def get_number(s):
    response = s.get("")
    if response.status_code==200:
        pattern = '<span id="page_queue_total">(\d+)</span>'
        result = re.compile(pattern).findall(response.text)
        number = result[0]
        n = int(number)
        return n
    else:
        print("Wrong")

#获取编辑中的url
def get_detail(s, url,banner_id):

    response = s.get(url)
    soup=BeautifulSoup(response.text, 'lxml')
    #print(soup)
    td=soup.select('td.formTd input#banners_url')
    href_url = td[0].get('value')

    olditem={banner_id:href_url}
    for i in olditem.items():
        #这是爬取下来的值
        k=i[0]
        v=i[1]
        # 插入方法
        get_insert(k,v)
        # 修改方法
        get_update(k,v)

#这是插入，判断如果爬取下来的值和数据库查询的值不相等的话，就进行插入
def get_insert(key,value):
    select = cursor.execute("select id from banner where id = %s",(key))
    result = cursor.fetchall()
    ke = str(result)


    if key not in ke:
        insert = cursor.execute('insert into banner value(%s,%s)',(key,value))
        conn.commit()
        urlbanner.append(value)
        print('插入')
    else:
        print('不插入')

#这是更新
def get_update(key,value):
    se_id = cursor.execute("select id from banner where id = %s",(key))
    result_id = cursor.fetchmany()
    ke = str(result_id)

    se_name = cursor.execute('select name from banner where id = %s',(key))
    result_name = cursor.fetchall()
    result = result_name[0][0]

    if key in ke:
        if value not in result:
            update = cursor.execute('update banner set name = %s where id = %s',(value,key))
            conn.commit()
            urlbanner.append(value)
            print('更新。。。。。')
        else:
            print('不更新')

#这是发送邮件
def email():

    #设置服务器（我这里是QQ的）
    smtpserver = 'smtp.qq.com'

    #设置用户名和密码，要登录邮箱的
    user = '@qq.com'
    password = ''

    #定义发送邮件和接收邮件的用户
    sender = user#这是发送用户
    receive=['']#这是接收用户


    #定义邮件的标题和内容
    subject = '【质管邮件--QA巡检】NC全站banner更新提醒日志'#这是标题


    content = """<html><body>
                <p>自动化测试项目相关信息</p>
                <p>(本邮件由程序自动下发，请勿回复！)</p>
                <p>每日固定11:00,15:00,20:00三个时间段定时检测</p>
                <p>本次监控目的是：</p>
                <p>若全站banner有更新上传,则检测其配置的链接是否可正常访问。</p>
                <p>(备注:状态码 200-400 ：banner链接访问正常; 状态码 400-600 : banner链接存在异常; 异常信息：链接访问较慢或非HTTPS)</p>
                <p>本次检查的报告如下：</p>
                <table width="50%" border="1" cellspacing="0" cellpadding="0">
                    <tr>
                        <td>banner的链接 </td>
                        <td>状态码</td>
                    </tr>"""



    for i in urlbanner:
        reponse = requests.get(i)
        res = str(reponse.status_code)
        content += """
                    <tr>
                        <td>"""+i+"""</td>
                        <td>"""+res+"""</td>
                    </tr>
                   """
    content +="""
                </table>
              </body>
              </html>"""#这是内容



    #接下来把上面的内容都装载
    msg = MIMEText(content,'html','utf-8')
    msg['Subject'] = Header(subject,'utf-8')
    msg['From']='@qq.com'
    msg['TO']=','.join(receive)

    smtp = smtplib.SMTP_SSL(smtpserver,465)
    smtp.helo(smtpserver)
    smtp.ehlo(smtpserver)
    smtp.login(user,password)

    print('Star send Email....')

    smtp.sendmail(sender,receive,msg.as_string())
    smtp.quit()
    print('Send Email end!')



if __name__=='__main__':
    get_html(login())
    email()

