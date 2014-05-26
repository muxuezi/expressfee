
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from PIL import Image
import os

# In[ ]:

PROV_FROM = [u'江苏省-南京市-栖霞区', u'广东省-广州市-花都区',u'天津市-天津市-东丽区', u'陕西省-西安市-新城区', u'四川省-成都市-龙泉驿区']

class Dstfee(object):

    """docstring for ClassName"""

    def __init__(self, url, addressfrom):
        self.url = url
        self.driver = webdriver.Chrome('./chromedriver')
        self.addressfrom = addressfrom
        self.PROV_TO = [arrivedCityName.strip() for arrivedCityName in open('zhongtongprov', 'rb').readlines()]

    def extract_and_ocr(self,dst,leftx,lefty,width,height):
        image_file = 'screenshot.png'
        img = Image.open(image_file)
        box = (leftx,lefty, leftx+width, lefty+height)
        img = img.crop(box)
        img.save('captcha.png')
        tatt=os.popen("./rpred.py -Q 4 -m %s.pyrnn.gz captcha.png" % dst)
        return tatt.read()[-5:-1]

    def getfeesf(self, addressto):
        def tempcapchar():
            self.driver.save_screenshot('screenshot.png')
            dst,leftx,lefty,width,height = 'zhongtong',485, 629, 50, 22 # zjs on x201i
#             code = self.extract_and_ocr(dst,leftx,lefty,width,height)
            code = raw_input('capchar?')
            self.driver.find_element_by_id("TextBoxCode").clear()
            self.driver.find_element_by_id("TextBoxCode").send_keys(code)
            self.driver.find_element_by_id("Button2").click()
        tempcapchar()
        while True:
            try:
                ft = self.driver.find_element_by_xpath('//*[@id="s_r"]/table/tbody/tr[4]/td[2]')
            except NoSuchElementException:
                tempcapchar()
            else:
                return ft.text.strip()
                break

    def feeoutput(self,fname,fee):
        self.driver.implicitly_wait(30)
        self.driver.get(self.url)
        addressfrom_prv, addressfrom_cty, addressfrom_are = self.addressfrom.split('-')
        Select(self.driver.find_element_by_id("s_province_text")).select_by_visible_text(addressfrom_prv[:-1])
        Select(self.driver.find_element_by_id("s_city_text")).select_by_visible_text(addressfrom_cty)
        self.driver.find_element_by_id("weight").clear()
        self.driver.find_element_by_id("weight").send_keys("1")
        def getfeex(addressto):
            addressto_prv, addressto_cty, addressto_are = addressto.split('-')
            Select(self.driver.find_element_by_id("m_province_text")).select_by_visible_text(addressto_prv)
            Select(self.driver.find_element_by_id("m_city_text")).select_by_visible_text(addressto_cty)
            fees = fee(addressto)
            return fees
        for idx,addressto in enumerate(self.PROV_TO):
            addressto = unicode(addressto.decode("utf-8"))
            fees = getfeex(addressto)
            print idx,addressto, fees
        self.driver.quit()

def last(add):
    url = 'http://www.zto.cn/Price.aspx'
    dstfee = Dstfee(url,add)
    dstfee.feeoutput(add+'_dst_fee_sf.txt', dstfee.getfeesf)

def main():
    map(last,PROV_FROM)

if __name__ == '__main__':
    main()


# In[ ]:



