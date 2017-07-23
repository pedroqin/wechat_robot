# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import sys
page = sys.argv[1]
url = 'http://www.qiushibaike.com/hot/page/' + str(page)
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = { 'User-Agent' : user_agent }
result=""
try:
    request = urllib2.Request(url,headers = headers)
    response = urllib2.urlopen(request)
    content = response.read().decode('utf-8')
    pattern = re.compile('<h2>(.*?)</h2>.*?<span>(.*?)</span>.*?</div>.*?</a>(.*?)<div class="stats">.*?class="number">(.*?)</i>.*?class="number">(.*?)</i>',re.S)
    items = re.findall(pattern,content)
    for item in items:
        haveImg = re.search("img",item[2])
        if not haveImg:
            replaceBR = re.compile('<br/>')
            text = re.sub(replaceBR,"\n",item[1])
#            print item[0],'\n',text,item[3],item[4],'\n'
            print item[0],'\n',text,u'\n 点赞数',item[3],u"\t 评论数",item[4],'\n'
#            result='\n'+text
            result=result+'\n'+text
#    print result
except urllib2.URLError, e:
    if hasattr(e,"code"):
        print e.code
    if hasattr(e,"reason"):
        print e.reason
