from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
import pandas as pd


REPORT_TABLES={'debt':'ZCFZB', 'profit':'GSLRB', 'main':'ZYCWZB', 'cash':'XJLLB'}
REPORT_URL='https://xueqiu.com/snowman/S/%s/detail#/%s'
INDEX_REPORT_ROWS=['营业收入','营业收入同比增长','净利润','净利润同比增长','净资产收益率','销售毛利率','资产负债率','总资产周转率','存货周转率','应收账款周转率']

def openBrowser():
    driver = webdriver.Firefox()
    return driver

def getYearlyReport(driver, stockNum,tableType,*indexRows):
    driver.get(REPORT_URL % (stockNum, REPORT_TABLES[tableType]))
    wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='年报']"))).click()
    table = driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div/div[4]/div/table')
    tablestr = '' + table.get_attribute('innerHTML')
    tablestr = '<table>%s</table>' % tablestr
    df = pd.read_html(tablestr)[0]
    df.columns = ['index', '2018年报', '2017年报', '2016年报', '2015年报', '2014年报']
    df.set_index('index', inplace=True)
    return df.loc[indexRows]


driver = openBrowser()
df=getYearlyReport(driver,'SZ001979','main',INDEX_REPORT_ROWS)
df.to_csv('E:\Project\cainiao\caibao\SZ001979.csv')



# assert "集思录" in driver.title
# peE=driver.find_element_by_xpath('//div[text()="PE"]')
# pePercent=peE.find_element_by_xpath('./following::div[contains(text(),"百分位")]').text
# pbE=driver.find_element_by_xpath('//div[text()="PB"]')
# pbPercent=pbE.find_element_by_xpath('./following::div[contains(text(),"百分位")]').text