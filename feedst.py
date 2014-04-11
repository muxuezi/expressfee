# -*- coding: utf-8 -*-


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import pyperclip
import time
from ABBYY import CloudOCR
from PIL import Image
from StringIO import StringIO
import re
import glob
from PIL import Image
import urllib2 as urllib
import io

APPLICATION_ID = 'fnord.tif'
PASSWORD = 'MhdQMuGh/pkLGyTTft5Wqm/D'
# PROV_FROM = [u"广东", u"江苏", u"陕西", u"四川", u"天津"]
# PROV_TO = [u"安徽", u"北京", u"福建", u"甘肃", u"广东", u"广西", u"贵州", u"海南", u"河北", u"河南", u"黑龙江", u"湖北", u"湖南", u"吉林", u"江苏", u"江西", u"辽宁", u"内蒙古", u"宁夏", u"青海", u"山东", u"山西", u"陕西", u"上海", u"四川", u"天津", u"西藏", u"新疆", u"云南", u"浙江", u"重庆"]
PROV_FROM = [u'江苏省-南京市-栖霞区', u'广东省-广州市-花都区',
             u'天津市-天津市-东丽区', u'陕西省-西安市-新城区', u'四川省-成都市-龙泉驿区']
PROV_TO = [arrivedCityName.strip()
           for arrivedCityName in open('arrivedCityName.txt', 'rb').readlines()]


def extract_and_ocr(codeurl):
    ocr_engine = CloudOCR(application_id=APPLICATION_ID, password=PASSWORD)
    # download code pic
    fd = urllib.urlopen(codeurl)
    image_file = io.BytesIO(fd.read())
    im = Image.open(image_file)
    # parse code
    region_data = image.convert('L')
    stream = StringIO()
    region_data.save(stream, 'JPEG')
    stream.seek(0)
    post_file = {'temp.jpg': stream}
    result = ocr_engine.process_and_download(post_file, exportFormat='txt')
    temp = result['txt'].read()
    return ''.join(re.split('\D', temp))


def getfeeems(addressfrom, addressto):
    Select(driver.find_element_by_id("addressfrom")
           ).select_by_value(addressfrom)
    Select(driver.find_element_by_id("addressto")).select_by_value(addressto)
    driver.find_element_by_name("weight").clear()
    driver.find_element_by_name("weight").send_keys("1")
    driver.find_element_by_class_name('table_btn').click()
    ft = driver.find_element_by_name("result")
    ft.send_keys(Keys.CONTROL, 'a')
    ft.send_keys(Keys.CONTROL, 'c')
    ft.send_keys(Keys.CONTROL, 'a')
    ft.send_keys(Keys.CONTROL, 'c')
    return pyperclip.paste()


def getfeeydkd(addressfrom, addressto):
    Select(driver.find_element_by_id("is_air")).select_by_visible_text(u"非航空件")
    Select(driver.find_element_by_id("sfd")
           ).select_by_visible_text(addressfrom)
    Select(driver.find_element_by_id("mdd")).select_by_visible_text(addressto)
    driver.find_element_by_name("zl").clear()
    driver.find_element_by_name("zl").send_keys("1")
    driver.find_element_by_xpath(u"//input[@value='查 询']").click()
    ft = driver.find_element_by_id("fy")
    return ft.text[:2]


def getfeedb(addressfrom, addressto):
    driver.find_element_by_id("leavedCityName").clear()
    driver.find_element_by_id("leavedCityName").send_keys(addressfrom)
    driver.find_element_by_id("arrivedCityName").clear()
    driver.find_element_by_id("arrivedCityName").send_keys(addressto)
    driver.find_element_by_xpath(u"//input[@value='查询']").click()
    try:
        ft = driver.find_elements_by_class_name("td_fir")
    except NoSuchElementException:
        return 'None'
    else:
        temp = [x.text for x in ft]
        return str(temp[-1]) if len(temp) == 4 else 'None'


def getfeedb(addressfrom, addressto):

    addressfrom_prv, addressfrom_cty, addressfrom_are = addressfrom.split('-')
    addressto_prv, addressto_cty, addressto_are = addressto.split('-')
    Select(driver.find_element_by_id("ctl00_Content1_Price_Province")
           ).select_by_visible_text(addressfrom_prv)
    Select(driver.find_element_by_id("City")
           ).select_by_visible_text(addressfrom_cty)
    Select(driver.find_element_by_id("Area")
           ).select_by_visible_text(addressfrom_are)
    try:
        Select(driver.find_element_by_id("ctl00_Content1_Price_RProvince")
               ).select_by_visible_text(addressto_prv)
        Select(driver.find_element_by_id("RCity")
               ).select_by_visible_text(addressto_cty)
        Select(driver.find_element_by_id("RArea")
               ).select_by_visible_text(addressto_are)
        driver.find_element_by_id("ctl00_Content1_Price_ZhongLiang").clear()
        driver.find_element_by_id(
            "ctl00_Content1_Price_ZhongLiang").send_keys("1")
        code = extract_and_ocr('http://www.zjs.com.cn/VerifyImg.aspx?')
        driver.find_element_by_id("ValidateTxt").clear()
        driver.find_element_by_id("ValidateTxt").send_keys(code)
        driver.find_element_by_id("Button1").click()
        ft = driver.find_elements_by_xpath(
            "/html/body/form/div[5]/div[2]/div[3]/table/tbody/tr/td/table[2]/tbody/tr/td/span/table/tbody/tr[3]/td[4]")
    except NoSuchElementException:
        return 'None'
    else:
        try:
            res = driver.find_elements_by_xpath('//*[@id="Result"]/font')
        except NoSuchElementException:
            return 'None'
        else:
            if u'验证码输入错误' in res.text:
                code = extract_and_ocr('http://www.zjs.com.cn/VerifyImg.aspx?')
                driver.find_element_by_id("ValidateTxt").clear()
                driver.find_element_by_id("ValidateTxt").send_keys(code)
                driver.find_element_by_id("Button1").click()
                ft = driver.find_elements_by_xpath(
                    "/html/body/form/div[5]/div[2]/div[3]/table/tbody/tr/td/table[2]/tbody/tr/td/span/table/tbody/tr[3]/td[4]")
            elif u'本公司暂未开通两地间快递服务' in res.text:
                return 'None'
            else:
                return ft.text


def feeoutput(fname, fee):
    pyperclip.setcb('0')
    with open(fname, 'wb') as f:
        for addressfrom in PROV_FROM:
            for addressto in PROV_TO:
                addressto = unicode(addressto.decode("utf-8"))
                driver.get(url)
                fees = fee(addressfrom, addressto)
                print addressto, fees
                f.write("%s\t%s\t%s\n" % (addressfrom.encode('utf-8'),
                        addressto.encode('utf-8'), fees.encode('utf-8')))


driver = webdriver.Chrome('./chromedriver')
driver.implicitly_wait(30)
t = raw_input('请确定平台物流商:1.EMS,2.韵达,3.德邦')
if t == '1':
    url = "http://www.yundaex.com/yunfei.html"
    feeoutput('dst_fee_ems.txt', getfeeems)
elif t == '2':
    url = "http://www.yundaex.com/yunfei.html"
    feeoutput('dst_fee_ydkd.txt', getfeeydkd)
elif t == '3':
    url = "http://www.deppon.com/jiageresult/"
    feeoutput('dst_fee_db.txt', getfeedb)
else:
    url = "http://www.zjs.com.cn/WS_Business/WS_Business_price_internal.aspx?id=6"
    feeoutput('dst_fee_zjs.txt', getfeedb)
