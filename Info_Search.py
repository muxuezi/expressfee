# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        info Search
# Purpose:      file download
# Python Version:       python2
# Author:      Arale Tao
#
# Created:     05-09-2014
# Copyright:   (c) Administrator 2014
# Licence:     All licence
#-------------------------------------------------------------------------------
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import re, sys, os, glob, datetime, pyperclip, time
reload(sys)
sys.setdefaultencoding('utf-8')

class SearchInfoWebKPy:
    def __init__(self, n_url):
        self.n_url = n_url
        self.lenhead = 0
        # self.driver = webdriver.Chrome('./chromedriver') # linux
        self.driver = webdriver.Chrome('chromedriver.exe') #windows
        self.download_location = ''
        self.searched_condition = ''
    def setdownloadlocation(self):
        driver = self.driver
        driver.get('chrome://settings/')
        driver.switch_to_frame(1)
        driver.find_element_by_id('advanced-settings-expander').click()
        time.sleep(1)
        driver.find_element_by_id('downloadLocationChangeButton').click()
        len_in = raw_input(u"请设置下载位置\n".encode('GBK'))
        if len_in == '':
            print(u'设置完毕')
        ft = driver.find_element_by_id('downloadLocationPath')
        def copyn(x):
            ft.send_keys(Keys.CONTROL, 'a')
            ft.send_keys(Keys.CONTROL, 'c')
        map(copyn,range(2))
        self.download_location = pyperclip.paste()
        return self.download_location

    def setup(self):
        self.driver.implicitly_wait(3)
        self.driver.get(self.n_url)
        self.driver.find_element_by_id('needMoreForNatural').click()
        df = self.driver.find_element_by_class_name('paragraph')
        self.searched_condition = df.text
        return self.searched_condition

    def allpage(self):
        driver = self.driver
        temp = driver.find_element_by_id('hitCount.top')
        total_num = int(''.join(re.findall('\d',temp.text)))
        # slice markFrom and markTo
        temp = []
        if total_num <= 500:
            temp.append((1,total_num))
        else:
            for t in range(1,total_num,500):
                markFrom = min(t,total_num)
                markTo = min(t + 499,total_num)
                temp.append((markFrom,markTo))
        len_t = len(temp)
        print(u"总共%d篇文献在数据库里，共需下载%d文本文件" % (total_num,len_t))
        len_in = raw_input(u"请输入下载起止页码(逗号分隔:如1,20)，全部下载请直接回车\n".encode('GBK'))
        if len_in == '':
            lenhead,lential = 1,len_t
            print(u'将下载全部文件')
        else:
            lenhead,lential = (int(x.strip()) for x in len_in.split(','))
            print(u'将下载第%d到%d页(%d-%d)之间的文件' % (lenhead,lential,temp[lenhead-1][0],temp[lential-1][1]))
        return temp,lenhead,lential

    def download_page(self,n):
        self.n = n # 如果n==2，纯文本，如果win==1，win+tab格式
        driver = self.driver
        temp,lenhead, lential = self.allpage()
        self.lenhead = lenhead
        try:
            Select(driver.find_element_by_id("saveToMenu")).select_by_value('other')
        except NoSuchElementException:
            print(u'网站改了，亲，HELP')

        for t in range(lenhead-1,lential):
            markFrom = str(temp[t][0])
            markTo = str(temp[t][1])
            driver.find_element_by_id("numberOfRecordsRange").click()
            driver.find_element_by_id("markFrom").send_keys(markFrom)
            driver.find_element_by_id("markTo").send_keys(markTo)
            #find the all style in bib_fields
            Select(driver.find_element_by_id("bib_fields")).select_by_index(3) #'Full Record and Cited References'

            if self.n == 1:
                Select(driver.find_element_by_id("saveOptions")).select_by_value('tabWinUnicode')
            else:
                Select(driver.find_element_by_id("saveOptions")).select_by_value('fieldtagged') #'Plain Text'

            if t == 0:
                print('%(id)d: From %(mfrom)s To %(mto)s download!' %{'id':t+1,'mfrom':markFrom,'mto':markTo})
            else:
                print('%(id)d: From %(mfrom)s To %(mto)s download!' %{'id':t+1,'mfrom':markFrom,'mto':markTo})

            driver.find_element_by_xpath("(//input[@name='email'])[4]").click()
            try:
                driver.find_element_by_name('formatForCancel').click()
            except NoSuchElementException:
                print(u'网站改了，亲，HELP')
            # 监控临时文件savedrecs.txt.crdownload，下载完成自动改名为markFrom-markTo.txt
            while True:
                if not filter(lambda x: x.rsplit('.')[-1] == 'crdownload', os.listdir(self.download_location)):
                    fd = os.path.join(self.download_location,'savedrecs.txt')
                    fto = os.path.join(self.download_location,'%s-%s.txt' % (str(markFrom),str(markTo)))
                    os.rename(fd,fto)
                    break
                time.sleep(0.1)
            Select(driver.find_element_by_id("saveToMenu")).select_by_value('other')
        driver.find_element_by_name('formatForCancel').click()

    def tearDown(self):
        self.driver.quit()

def mk_clear_all(output_location):
    if not os.path.exists(output_location):                  # caller handles errors
        os.mkdir(output_location)                            # make dir, read/write parts
    else:
        for fname in os.listdir(output_location):            # delete any existing files
            os.remove(os.path.join(output_location, fname))

def main():
    print(u"此版本为自定义模式")
    root_file = os.getcwd()
    n_load = raw_input(u"下载纯文本,直接回车;下载win+tab格式文本，请输入1,再回车\n".encode('GBK'))
    n_url = open('config.ini').read().strip()
    sear = SearchInfoWebKPy(n_url)
    # 下载文件从chrome获取
    download_location = sear.setdownloadlocation()
    output_location = re.sub('[-:\s]','',str(datetime.datetime.now()).split('.')[0])
    print u"下载文件将放在%s\n" % download_location
    #启动程序并获得搜索条件
    searched_condition = sear.setup()
    fna = '%s_search_condition.dat' % output_location
    # 如果n==2，纯文本，如果win==1，win+tab格式
    if n_load == '1':sear.download_page(1)
    else:sear.download_page(2)
    sear.tearDown() # chrome quit
    os.chdir(download_location) # enter in download file
    with open(fna,'w') as f:
        for p in searched_condition.split('\n')[:-1]:
            f.write(p+'\n')
    mk_clear_all(output_location) #生成文件夹
    from_temp = glob.glob(download_location + r'/' + '*.txt')
    for ft in from_temp:
        mv_path = os.path.join(output_location, os.path.basename(ft))
        os.rename(ft,mv_path) # move txt to output_location
    print u'所有txt已经移动到%s' % output_location
    os.chdir(root_file)
    raw_input(u'回车退出'.encode('GBK')) # pause if clicked

if __name__ == "__main__":
    main()

