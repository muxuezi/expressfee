# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>


from bs4 import BeautifulSoup
import urllib2
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import *


class SchoolName(object):

    """docstring for ClassName"""

    def __init__(self, argp0, argp1):
        self.argp0 = argp0
        self.argp1 = argp1
        self.baseurl = "http://kaoshi.edu.sina.com.cn/abroad/list.php?country=&type=&zhinanflag=&collegename=&page="
        self.temp = []

    def catch_txt(self, purl):
        print 'page in: %s' % str(purl + 1)
        url = self.baseurl + str(purl + 1)
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page.read())
        table = soup.find('table', attrs={'bgcolor': "#ABBEE6"})
        rows = table.findAll(lambda tag: tag.name == 'tr')
        return enumerate(rows[1:])

    def contactFrame(self, url):
        page = urllib2.urlopen(url)
        esoup = BeautifulSoup(page.read())
        ename = esoup.find('table', attrs={'width': "98%"}).text
        txt = ename.strip().split('\r\n')
        if len(txt) == 1:
            if 'contactFrame' in esoup.get_text():
                driver = webdriver.Chrome('./chromedriver')
                driver.implicitly_wait(10)
                driver.get(url)
                try:
                    driver.switch_to_frame('contactFrame')
                    name = driver.find_element_by_xpath(
                        '/html/body/div[1]/div/div/div[2]/h4')
                except UnexpectedAlertPresentException or NoSuchElementException:
                    driver.quit()
                    return 'None'
                else:
                    txt = name.text.strip().split('\r\n')
                    driver.quit()
                    return txt[-1].strip() if len(txt) > 1 else 'None'
            else:
                return 'None'

        else:
            return txt[-1].strip()

    def gettext(self, page, idx, row):
        itemid = str(page * 20 + idx + 1)
        schtext = row.text.strip().split('\n')
        url = row.find('a', attrs={'target': "_blank"}).get('href')
        # nameoutput = self.contactFrame(url)
        nameoutput = 'None'
        output = [itemid, nameoutput] + schtext[:-1] + [url]
        return output

    def outxlsx(self):
        
        fname = 'schoolname_%s_%s.xlsx' % (str(self.argp0), str(self.argp1))
        for upage in range(self.argp0, self.argp1):
            for idx, row in self.catch_txt(upage):
                schoolinfo = self.gettext(upage, idx, row)
                print schoolinfo[0],schoolinfo[2]
                self.temp.append(schoolinfo)
        df = pd.DataFrame(self.temp, columns=['id', u'院校名称', u'中文名称', u'国家', u'城市', u'类别', 'url', ''])
        df.to_excel(fname, u'国外高校', index=False)


if __name__ == '__main__':
    s = SchoolName(0,678)
    s.outxlsx()
