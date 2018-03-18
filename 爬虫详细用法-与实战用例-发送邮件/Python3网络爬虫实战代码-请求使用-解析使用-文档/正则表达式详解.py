
import re
import requests


content = requests.get('https://book.douban.com/').text
patter = re.compile('<li.*?cover.*?>.*?</li>',re.S)
result = re.findall(patter,content)
print(result)

for ss in result:

    print(ss)




#实战
# content = requests.get('https://book.douban.com/').text
# patterm = re.compile('<li.*?cover.*?href="(.*?)".*?title="(.*?)".*?more-ta.*?author">(.*?)</span>.*?year">(.*?)</span>.*?</li>',re.S)
# result  = re.findall(patterm,content)
# for results in result:
#     url,name,author,date = results
#     print(url,name,author,date)

