# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>


from multiprocessing import Pool
from bs4 import BeautifulSoup
import urllib2
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


baseurl = "http://kaoshi.edu.sina.com.cn/abroad/list.php?country=&type=&zhinanflag=&collegename=&page="


def catch_ename(url):
    print 'page in: %d' % url
    url = baseurl + str(url + 1)
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page.read())
    table = soup.find('table', attrs={'bgcolor': "#ABBEE6"})
    rows = table.findAll(lambda tag: tag.name == 'tr')
    return enumerate(rows[1:])


def gettext(idx, row):
    url = row.find('a', attrs={'target': "_blank"}).get('href')
    page = urllib2.urlopen(url)
    esoup = BeautifulSoup(page.read())
    ename = esoup.find('table', attrs={'width': "98%"}).text
    itemid = str(url * 20 + idx)
    output = '\t'.join(ename.strip().split('\r\n').insert(0, itemid)) + '\n'
    return output


if __name__ == '__main__':

    pool = Pool(4)
    alltd = pool.map(catch_ename, range(600, 678))
    pool.close()
    pool.join()

    pool = Pool(4)
    result = pool.map(gettext, alltd)
    pool.close()
    pool.join()    

    with open('ename3.txt', 'wb') as f:
        for res in result:
            f.write(result)
