from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
import pandas as pd
import tushare as ts


INDEX_REPORT_ROWS=['营业收入','营业收入同比增长','净利润','净利润同比增长','净资产收益率','销售毛利率','资产负债率','总资产周转率','存货周转率','应收账款周转率']
PROFIT_STATEMENT_ROWS=['营业利润','利润总额','净利润']
BALANCE_SHEET_ROWS=['非流动资产合计','资产合计']
CASH_FLOW_ROWS=['经营活动产生的现金流量净额']

REPORT_TABLES={'balance':'ZCFZB', 'profit':'GSLRB', 'main':'ZYCWZB', 'cash':'XJLLB'}
REPORT_ROWS={'balance':BALANCE_SHEET_ROWS, 'profit':PROFIT_STATEMENT_ROWS, 'main':INDEX_REPORT_ROWS, 'cash':CASH_FLOW_ROWS}
XQ_REPORT_URL='https://xueqiu.com/snowman/S/%s/detail#/%s'
JSL_REPORT_URL='https://www.jisilu.cn/data/stock/%s'

def openBrowser():
    driver = webdriver.Firefox()
    return driver


def getPercent(scode,driver=openBrowser()):
    driver.get(JSL_REPORT_URL % (scode))
    assert "集思录" in driver.title
    peE = driver.find_element_by_xpath('//div[text()="PE"]')
    pePercent = peE.find_element_by_xpath('./following::div[contains(text(),"百分位")]').text
    pbE = driver.find_element_by_xpath('//div[text()="PB"]')
    pbPercent = pbE.find_element_by_xpath('./following::div[contains(text(),"百分位")]').text
    return {'pePercent':pePercent,'pbPercent':pbPercent}


def writeAllXQReports(scode):
    fname = "E:\Project\stocks\\reports\\" + scode + ".xlsx"
    with pd.ExcelWriter(fname) as writer:
        for type in REPORT_TABLES.keys():
            driver = openBrowser()
            df = getYearlyReport(driver, scode, type)
            df.to_excel(writer, sheet_name=type)

def getYearlyReport(stockNum,tableType,driver=openBrowser()):
    driver.get(XQ_REPORT_URL % (stockNum, REPORT_TABLES[tableType]))
    wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='年报']"))).click()
    table = driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div/div[4]/div/table')
    tablestr = '' + table.get_attribute('innerHTML')
    tablestr = '<table>%s</table>' % tablestr
    df = pd.read_html(tablestr)[0]
    df.columns = ['index', '2018年报', '2017年报', '2016年报', '2015年报', '2014年报']
    df.set_index('index', inplace=True)
    return df.loc[REPORT_ROWS[tableType]]

def getAllCode():
    pro = ts.pro_api()
    data=pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    return data




