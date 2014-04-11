# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from bs4 import BeautifulSoup
import urllib2
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# <codecell>

baseurl="http://kaoshi.edu.sina.com.cn/abroad/list.php?country=&type=&zhinanflag=&collegename=&page="
# url = 0
page = range(60)
with open('ename0.txt','wb') as f:
    for url in page:
        print 'page in:',url
        url = baseurl + str(url+1)
        page=urllib2.urlopen(url)
        soup = BeautifulSoup(page.read())
        table = soup.find('table',attrs={'bgcolor':"#ABBEE6"})
        rows = table.findAll(lambda tag: tag.name=='tr')
        for row in rows[1:]:
    #         print '\t'.join(row.text.split('\n')[:-3])
            url = row.find('a',attrs={'target':"_blank"}).get('href')
    #         print url
            page=urllib2.urlopen(url)
            esoup = BeautifulSoup(page.read())
            ename = esoup.find('table',attrs={'width':"98%"}).text
    #         print ename
            output = '\t'.join(ename.strip().split('\r\n'))
            f.write( output +'\n' )


# <codecell>


