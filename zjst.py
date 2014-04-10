from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re

class Zjst(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://www.zjs.com.cn/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_zjst(self):
        driver = self.driver
        driver.get(self.base_url + "/WS_Business/WS_Business_price_internal.aspx?id=6")
        # ERROR: Caught exception [ReferenceError: selectLocator is not defined]
        # ERROR: Caught exception [ReferenceError: selectLocator is not defined]
        # ERROR: Caught exception [ReferenceError: selectLocator is not defined]
        # ERROR: Caught exception [ReferenceError: selectLocator is not defined]
        # ERROR: Caught exception [ReferenceError: selectLocator is not defined]
        # ERROR: Caught exception [ReferenceError: selectLocator is not defined]
        driver.find_element_by_id("ctl00_Content1_Price_ZhongLiang").clear()
        driver.find_element_by_id("ctl00_Content1_Price_ZhongLiang").send_keys("1")
        driver.find_element_by_id("ValidateTxt").clear()
        driver.find_element_by_id("ValidateTxt").send_keys("1541")
        driver.find_element_by_id("Button1").click()
        driver.find_element_by_css_selector("richlistitem[name=\"Firebug\"]").click()
        # ERROR: Caught exception [ERROR: Unsupported command [selectWindow | name=fbMainContainer | ]]
        driver.find_element_by_id("fbInspectButton").click()
        driver.find_element_by_id("fbInspectButton").click()
        driver.find_element_by_id("fbInspectButton").click()
        driver.find_element_by_id("fbInspectButton").click()
        driver.find_element_by_id("fbToggleHTMLEditing").click()
        driver.find_element_by_id("fbToggleHTMLEditing").click()
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
