
# coding: utf-8

# In[7]:


from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import os,time
from PIL import Image


# In[6]:

PROV_FROM = [u'江苏省-南京市-栖霞区', u'广东省-广州市-花都区',u'天津市-天津市-东丽区', u'陕西省-西安市-新城区', u'四川省-成都市-龙泉驿区']

class Dstfee(object):

    """docstring for ClassName"""

    def __init__(self, url, addressfrom):
        self.url = url
        self.driver = webdriver.Chrome('./chromedriver')
        self.addressfrom = addressfrom
        self.PROV_TO = [arrivedCityName.strip() for arrivedCityName in open('sfprov', 'rb').readlines()]

    def extract_and_ocr(self,dst,leftx,lefty,width,height):
        image_file = 'screenshot.png'
        img = Image.open(image_file)
        box = (leftx,lefty, leftx+width, lefty+height)
        img = img.crop(box)
        self.pngtrans(img) # transfer
        tatt=os.popen("./rpred.py -Q 4 -m %s.pyrnn.gz captcha.png" % dst)
        return tatt.read()[-5:-1]

    def pngtrans(self,img):
        img1 = img.crop((15,0,30,25))
        img2 = img.crop((30,0,45,25))
        img3 = img.crop((45,0,60,25))
        img1 = img1.offset(xoffset=0,yoffset=2)
        img2 = img2.offset(xoffset=0,yoffset=-1)
        img3 = img3.offset(xoffset=0,yoffset=1)
        img.paste(img1,box=(15,0))
        img.paste(img2,box=(30,0))
        img.paste(img3,box=(45,0))
        img0 = img.crop((0,6,60,22))
        img0.save('captcha.png')

    def getfeesf(self,addressfrom, addressto):
        def tempcapchar():
            self.driver.save_screenshot('screenshot.png')
            dst,leftx,lefty,width,height = 'shunfeng',319, 230,60,25 # zjs on x201i
            # code = self.extract_and_ocr(dst,leftx,lefty,width,height)
            code = raw_input('capchar?')
            self.driver.find_element_by_id("verifycode_china").clear()
            self.driver.find_element_by_id("verifycode_china").send_keys(code)
            self.driver.find_element_by_id("btnEnquiry_china").click()

        addressfrom_prv, addressfrom_cty, addressfrom_are = addressfrom.split('-')
        addressto_prv, addressto_cty, addressto_are = addressto.split('-')
        Select(self.driver.find_element_by_id("originProvinceChina")).select_by_visible_text(addressfrom_prv[:-1])
        Select(self.driver.find_element_by_id("originCityChina")).select_by_visible_text(addressfrom_cty)
        Select(self.driver.find_element_by_id("destinationProvinceChina")).select_by_visible_text(addressto_prv)
        Select(self.driver.find_element_by_id("destinationCityChina")).select_by_visible_text(addressto_cty)
        tempcapchar()
        while True:
            try:
                lufei = self.driver.find_element_by_id("errorMsgTxt_china")
            except NoSuchElementException:
                break
            else:
                time.sleep(1)
                if lufei.text: tempcapchar()
                else:break
        try:
            ft = self.driver.find_element_by_id('resuleTextTD_priceW')
            return ft.text.strip().split()[-1]
        except NoSuchElementException:
            return 'None'

    def feeoutput(self,fname,fee):
        def getfeex(addressto):
            self.driver.implicitly_wait(30)
            addressto = unicode(addressto.decode("utf-8"))
            self.driver.get(self.url)
            if 'sf-express' in self.url:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/1.8);")
                self.driver.switch_to_frame('frame_content') # shunfeng
                self.driver.find_element_by_id("itemWeightChina").clear()
                self.driver.find_element_by_id("itemWeightChina").send_keys("1")
            fees = fee(self.addressfrom, addressto)
            return fees
        for idx,addressto in enumerate(self.PROV_TO):
            fees = getfeex(addressto)
            print idx+15,addressto, fees
        self.driver.quit()

def last(add):
    url = 'http://www.sf-express.com/cn/sc/delivery_step/enquiry/rate_enquiry.html'
    dstfee = Dstfee(url,add)
    dstfee.feeoutput('dst_fee_sf.txt', dstfee.getfeesf)

def main():
    map(last,PROV_FROM[1:2])
if __name__ == '__main__':
    main()

