import pandas as pd
import tushare as ts
import time
today=time.strftime("%Y%m%d", time.localtime())

PROFESSION=['op_to_ebt'] #营业利润/税前利润总额
OPERATE=['grossprofit_margin']
EFF=['assets_turn','inv_turn','ar_turn'] #总资产周转率，存货周转率，应收账款周转率
RISK=['nca_to_assets'] #非流动资产占比
DEBT=['debt_to_assets','int_to_talcap','current_exint','noncurrent_exint','interestdebt'] #负债率，带息债务率，无息流动负债,无息非流动负债,
PERFORM=['roe']

global pro
pro = ts.pro_api()

def getAllCode(bday):
    sbasic=pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date,market')
    dbasic=pro.query('daily_basic', ts_code='', trade_date=bday,
                     fields='ts_code,trade_date,pe,pb,total_share,float_share,total_mv,circ_mv')
    data=pd.merge(sbasic, dbasic, on='ts_code')
    return data

def getStockName(tscode):
    df=pro.query('stock_basic',exchange='', list_status='L', fields='ts_code,name')
    return df[df.ts_code==tscode].iloc[0,1]

def getTopByIndustry(industry,top,bday,sort_value='total_mv'):
    data=getAllCode(bday)
    datanew=data[data['industry'].str.contains(industry)].sort_values(by=sort_value, ascending=False)[['ts_code','name']]
    return datanew[:top]

def transScode(num):
    d={
        '00':'SZ',
        '30':'SZ',
        '60':'SH'
    }
    return d[num[:2]]+num


def getYearlyIndicator(tscode,tsname,col):
    df = pro.fina_indicator(ts_code=tscode)
    df = df[df.end_date.str.contains('1231')][['end_date'] + col].head(6)
    for nm in df.colummns:
        df.rename(columns={nm: nm + '_' + tsname}, inplace=True)
    return df

bj_list=getTopByIndustry('白酒',15)



# ind='baijiu'
# path="E:\Project\stocks\\reports\\"+ind+"\\"




