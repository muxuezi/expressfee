package com.example.tests;

import java.util.regex.Pattern;
import java.util.concurrent.TimeUnit;
import org.junit.*;
import static org.junit.Assert.*;
import static org.hamcrest.CoreMatchers.*;
import org.openqa.selenium.*;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.support.ui.Select;

public class Zjstest {
  private WebDriver driver;
  private String baseUrl;
  private boolean acceptNextAlert = true;
  private StringBuffer verificationErrors = new StringBuffer();

  @Before
  public void setUp() throws Exception {
    driver = new FirefoxDriver();
    baseUrl = "http://www.zjs.com.cn/";
    driver.manage().timeouts().implicitlyWait(30, TimeUnit.SECONDS);
  }

  @Test
  public void testZjs() throws Exception {
    driver.get(baseUrl + "/WS_Business/WS_Business_price_internal.aspx?id=6");
    new Select(driver.findElement(By.id("ctl00_Content1_Price_Province"))).selectByVisibleText("安徽省");
    new Select(driver.findElement(By.id("City"))).selectByVisibleText("安庆市");
    new Select(driver.findElement(By.id("Area"))).selectByVisibleText("枞阳县");
    new Select(driver.findElement(By.id("ctl00_Content1_Price_RProvince"))).selectByVisibleText("安徽省");
    new Select(driver.findElement(By.id("RCity"))).selectByVisibleText("安庆市");
    new Select(driver.findElement(By.id("RArea"))).selectByVisibleText("枞阳县");
    driver.findElement(By.id("ctl00_Content1_Price_ZhongLiang")).clear();
    driver.findElement(By.id("ctl00_Content1_Price_ZhongLiang")).sendKeys("1");
    driver.findElement(By.id("ValidateTxt")).clear();
    driver.findElement(By.id("ValidateTxt")).sendKeys("1541");
    driver.findElement(By.id("Button1")).click();
  }

  @After
  public void tearDown() throws Exception {
    driver.quit();
    String verificationErrorString = verificationErrors.toString();
    if (!"".equals(verificationErrorString)) {
      fail(verificationErrorString);
    }
  }

  private boolean isElementPresent(By by) {
    try {
      driver.findElement(by);
      return true;
    } catch (NoSuchElementException e) {
      return false;
    }
  }

  private boolean isAlertPresent() {
    try {
      driver.switchTo().alert();
      return true;
    } catch (NoAlertPresentException e) {
      return false;
    }
  }

  private String closeAlertAndGetItsText() {
    try {
      Alert alert = driver.switchTo().alert();
      String alertText = alert.getText();
      if (acceptNextAlert) {
        alert.accept();
      } else {
        alert.dismiss();
      }
      return alertText;
    } finally {
      acceptNextAlert = true;
    }
  }
}
