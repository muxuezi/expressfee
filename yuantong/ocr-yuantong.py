# coding: utf-8

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import os
from PIL import Image


PROV_FROM = [u'江苏省-南京市-栖霞区', u'广东省-广州市-花都区',u'天津-天津市-东丽区', u'陕西省-西安市-新城区', u'四川省-成都市-龙泉驿区']

class Dstfee(object):

    """docstring for ClassName"""

    def __init__(self, url, addressfrom):
        self.url = url
        self.driver = webdriver.Chrome('./chromedriver')
        self.addressfrom = addressfrom
        self.PROV_TO = [arrivedCityName.strip() for arrivedCityName in open('yuantongprov', 'rb').readlines()]

    def extract_and_ocr(self,dst,leftx,lefty,width,height):
        image_file = 'screenshot.png'
        png_file = 'captcha.png'
        img = Image.open(image_file)
        box = (leftx,lefty, leftx+width, lefty+height)
        img = img.crop(box)
        img0 = img.convert("L")
        img1 = img0.point(lambda i: 0 if i < 120 else 255)
        img1.save(png_file)
        tatt=os.popen("./rpred.py -Q 4 -m %s.pyrnn.gz %s" % (dst,png_file))
        return tatt.read()[-5:-1]

    def getfeeyuantong(self,addressfrom, addressto):
        addressfrom_prv, addressfrom_cty, addressfrom_are = addressfrom.split('-')
        addressto_prv, addressto_cty, addressto_are = addressto.split('-')

        def tempcapchar():
            self.driver.save_screenshot('screenshot.png')
            dst,leftx,lefty,width,height = 'yuantong',  572,  534, 57, 22
            code = self.extract_and_ocr(dst,leftx,lefty,width,height)
            self.driver.find_element_by_id("Verfity").clear()
            self.driver.find_element_by_id("Verfity").send_keys(code)
            self.driver.find_element_by_xpath("//div/li/a/span").click()

        def pageload():
            Select(self.driver.find_element_by_id("selPro")).select_by_visible_text(addressfrom_prv)
            Select(self.driver.find_element_by_id("selCity")).select_by_visible_text(addressfrom_cty)
            Select(self.driver.find_element_by_id("selDis")).select_by_visible_text(addressfrom_are)
            Select(self.driver.find_element_by_id("desPro")).select_by_visible_text(addressto_prv)
            Select(self.driver.find_element_by_id("desCity")).select_by_visible_text(addressto_cty)
            Select(self.driver.find_element_by_id("desDis")).select_by_visible_text(addressto_are)
            self.driver.find_element_by_id("txtexpressWeight").clear()
            self.driver.find_element_by_id("txtexpressWeight").send_keys("1")
        pageload()
        tempcapchar()
        while True:
            try:
                lufei = self.driver.find_element_by_id("verfityFont")
            except NoSuchElementException:
                break
            else:
                if lufei.text:
                    self.driver.refresh()
                    pageload()
                    tempcapchar()
                else:break
        try:
            ft = self.driver.find_element_by_xpath('//*[@id="labprice"]/span/span')
            return ft.text.strip()
        except NoSuchElementException:
            return 'None'
    def feeoutput(self,fname,fee):
        def getfeex(addressto):
            self.driver.implicitly_wait(3)
            addressto = unicode(addressto.decode("utf-8"))
            self.driver.get(self.url)
            fees = fee(self.addressfrom, addressto)
            return fees
        for idx,addressto in enumerate(self.PROV_TO):
            fees = getfeex(addressto)
            print idx, addressto, fees
        self.driver.quit()
def last(add):
      url = "http://www.yto.net.cn/cn/service/standardPrice.html"
      dstfee = Dstfee(url,add)
      dstfee.feeoutput('dst_fee_yuantong.txt', dstfee.getfeeyuantong)
def main():
    map(last,PROV_FROM)
if __name__ == '__main__':
    main()
