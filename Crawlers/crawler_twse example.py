import requests
import pandas as pd
import io
import re
import time
import datetime

"""用來爬證券交易所網站的資料"""
def crawler(date_time):
    page_url = 'http://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + date_time +'&type=ALLBUT0999' #觀察網址
    page = requests.get(page_url) #建立requests物件
    use_text = page.text.splitlines()
    for i,text in enumerate(use_text): #i是位置 text是那行的string, 第i行存放的string是text
        if text == '"證券代號","證券名稱","成交股數","成交筆數","成交金額","開盤價","最高價","最低價","收盤價","漲跌(+/-)","漲跌價差","最後揭示買價","最後揭示買量","最後揭示賣價","最後揭示賣量","本益比",':
            initial_point = i #前面有不需要的資訊 讓爬蟲爬到關鍵句後再開始讀資訊 記下關鍵行數
            break
    test_df = pd.read_csv(io.StringIO(''.join([text[:-1] + '\n' for text in use_text[initial_point:]]))) #原本: ="0050","元大台灣50","3,021,521","4,359","413,571,142","137.30","137.50","136.50","136.50","-","0.80","136.50","479","136.55","28","0.00",
	#text[:-1](不包含倒數第一項)把最後的,去掉 #只用從第initial_point行之後的text #str1.join(str2)是把它們串起來  #去,: ="0050","元大台灣50","3,021,521","4,359","413,571,142","137.30","137.50","136.50","136.50","-","0.80","136.50","479","136.55","28","0.00"
    test_df['證券代號'] = test_df['證券代號'].apply(lambda x: x.replace('"','')) #去"
    test_df['證券代號'] = test_df['證券代號'].apply(lambda x: x.replace('=','')) #去=
    return test_df
	
"""把一個datetime物件轉換成2020308的string"""
def trans_date(date_time): #datetime格式為2002-03-08 00:00:00
    return ''.join(str(date_time).split(' ')[0].split('-')) #str(date_time).split(' ')[0] -> 2002-03-08, join -> 20020308

"""return在start_date(datetime物件)前n天的證券資料"""
def parse_n_days(start_date,n):
    df_dict = {} #dictionary, key是date(e.g.20020308), value是df list(給定日期crawler給的證券資料)(e.g.很多行像"0050","元大台灣50","3,021,521","4,359"...)
    now_date = start_date #紀錄開始時間 now_date會改
    for i in range(n):
        time.sleep(5)
        now_date = now_date - datetime.timedelta(days=1) #往前推一天
        print("\nday "+str(i+1)+":") 
        try:
            df = crawler(trans_date(now_date)) #crawler找當天的證券資料df list, index是'證券代號' value是一行很多的指標
            df_dict.update({trans_date(now_date):df}) #添加key為日期 value是df list
            print('Success:',str(now_date.strftime('%Y%m%d')),"weekday")
        except:
            print('Fail:' ,str(now_date.strftime('%Y%m%d')),"weekend")
    return df_dict

"""測試crawler_twse_v1"""
date = datetime.datetime.strptime("20210606","%Y%m%d") 
print(parse_n_days(date,3).keys())
print(parse_n_days(date,3).values())
"""source: https://github.com/pyinvest/python_finance_tutorial/blob/master/gentle_start/EP1_%E6%8A%93%E8%B3%87%E6%96%99.ipynb """