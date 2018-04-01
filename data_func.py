# -*- coding: utf-8 -*-
"""
@ Time    : 2018-03-28 21:01
@ author  : weixiang
@ FileName: PTA_data.py
@ User    : 魏翔
@ desc    :

数据清洗和分析

1、将数据源清洗合并到本地数据库，每日更新
2、将本地数据库插入多列，生成分钟线，MACD等指标；
3、分析长短趋势；

"""
import pandas as pd
import linecache

def get_k_date(hour, minute, seconds, mi_seconds, k_period, is_night, night_second=7200):
    """

    :param hour:
    :param minute:
    :param seconds:
    :param mi_seconds:
    :param k_period:
    :param is_night:
    :param night_second:    # 默认7200 即23：00收盘； 23：30收盘即9000；
    :return:
    """
    time_seconds = 0
    Index = 0
    if is_night:
        if hour == 9 or (hour == 10 and minute <= 15):
            time_seconds = (hour - 9) * 3600 + minute * 60 + seconds * 1 + night_second + mi_seconds
        elif hour == 11 or (hour == 10 and minute >= 30):
            time_seconds = (hour - 9) * 3600 + minute * 60 + seconds * 1 + night_second - 900 + mi_seconds
        elif hour >= 13 and hour < 15:
            time_seconds = (hour - 9) * 3600 + minute * 60 + seconds * 1 + night_second - 900 - 2 * 3600 + mi_seconds
        elif hour >= 15:
            time_seconds = (15 - 9) * 3600 + minute * 60 + seconds * 1 + night_second - 900 - 2 * 3600 + mi_seconds

    else:
        if hour == 9 or (hour == 10 and minute <= 15):
            time_seconds = (hour - 9) * 3600 + minute * 60 + seconds * 1 + mi_seconds
        elif hour == 11 or (hour == 10 and minute >= 30):
            time_seconds = (hour - 9) * 3600 + minute * 60 + seconds * 1 - 900 + mi_seconds
        elif hour >= 13 and hour < 15:
            time_seconds = (hour - 9) * 3600 + minute * 60 + seconds * 1 - 900 - 2 * 3600 + mi_seconds

    if k_period > 0:
        Index = int(time_seconds / k_period)
    else:
        print("k_period can not be <=0 ")
    return Index

# 服务器接受行情
# raw = pd.read_table("E:\\python_code\\tem_chen\\TA_data\\TA805#20180327.txt", sep=";", header=None)
# raw.head()
# code = raw.columns
# sample = raw.loc[:, [0，8,15,16,17,18,19,20]]
# sample.head()
# sample.tail()
# selectData = []

instrument = "20180327"
filename = "E:\\python_code\\tem_chen\\TA_data\\TA805#{0}.txt".format(instrument)
cach_data = linecache.getlines(filename)
night = True
nitghtsecond=9000
kperiod = 60
tem_index = 0
volume=[]
timesecond=0
openprice = 0
highPrice = 0
lowPrice = 9999999
closeprice = 0
Kvol=0

openP=[]
highP=[]
lowP=[]
closeP=[]
xline=[]
GK=[]
selectData = []
# 波动率
GKvolatility=0

for x in range(3, len(cach_data)):
    data_arr_main = cach_data[x].split(';')
    temx_time = str(data_arr_main[15]).split(':')

    hour = int(temx_time[0])
    mininuts = int(temx_time[1])
    seconds = int(temx_time[2])
    temmiSeconds =int(data_arr_main[16])

    temTradingDay = str(data_arr_main[0])
    temUpdateTime = str(data_arr_main[15])
    tembidprice = float(data_arr_main[17])
    temaskprice = float(data_arr_main[19])
    tembidvolume = float(data_arr_main[18])
    temaskvolume = float(data_arr_main[20])
    temlastprice = float(data_arr_main[2])
    temtradevolume = float(data_arr_main[8])
    temopeninterest = float(data_arr_main[10])

    volume.append(temtradevolume)

    miSeconds=0.5 if temmiSeconds > 1 else 0


    if (hour >= 21 and hour <= 24):
        timesecond = (hour - 21) * 3600 + mininuts * 60 + seconds * 1 + miSeconds
    elif (hour >= 0 and hour <= 2):
        timesecond = 10800 + hour * 3600 + mininuts * 60 + seconds * 1 + miSeconds
    elif (hour >= 9 and hour < 15):
        # 有夜盘，K线从昨天开始算起
        if (night):
            if (hour == 9 or (hour == 10 and mininuts <= 15)):
                timesecond = (hour - 9) * 3600 + mininuts * 60 + seconds * 1 + nitghtsecond + miSeconds
            elif (hour == 11 or (hour == 10 and mininuts >= 30)):
                timesecond = (hour - 9) * 3600 + mininuts * 60 + seconds * 1 + nitghtsecond - 900 + miSeconds
            elif (hour >= 13 and hour < 15):
                timesecond = (hour - 9) * 3600 + mininuts * 60 + seconds * 1 + nitghtsecond - 900 - 2 * 3600 + miSeconds
        else:
            if (hour == 9 or (hour == 10 and mininuts <= 15)):
                timesecond = (hour - 9) * 3600 + mininuts * 60 + seconds * 1 + miSeconds
            elif (hour == 11 or (hour == 10 and mininuts >= 30)):
                timesecond = (hour - 9) * 3600 + mininuts * 60 + seconds * 1 - 900 + miSeconds
            elif (hour >= 13 and hour < 15):
                timesecond = (hour - 9) * 3600 + mininuts * 60 + seconds * 1 - 900 - 2 * 3600 + miSeconds

    Index = int(timesecond / kperiod)
    tick_Vol=(temtradevolume-volume[-2]) if len(volume)>=2 else temtradevolume

    if (tem_index != Index):
        # 计算上一个K线波动率
        GKvolatility = 0.5 * (highPrice - lowPrice) * (highPrice - lowPrice) - 0.38629436111989 * (
            closeprice - openprice) * (closeprice - openprice)

        tem_index = Index  # 一根K线内
        openprice = temlastprice
        highPrice = temaskprice
        lowPrice = tembidprice
        closeprice = temlastprice
        Kvol=temtradevolume

        openP.append(openprice)
        highP.append(highPrice)
        lowP.append(lowPrice)
        closeP.append(closeprice)
        xline.append(x)
        GK.append(GKvolatility)


    else:
        closeprice=temlastprice
        if(temaskprice>=highPrice):
            highPrice=temaskprice
        if(tembidprice<=lowPrice):
            lowPrice=tembidprice

        openP.append(openprice)
        highP.append(highPrice)
        lowP.append(lowPrice)
        closeP.append(closeprice)
        xline.append(x)
        GK.append(GKvolatility)


    selectData.append([temTradingDay, temUpdateTime, tembidprice, tembidvolume, temaskprice, temaskvolume, temlastprice,
         temtradevolume,tick_Vol ,temopeninterest,timesecond,Index,openprice,highPrice,lowPrice,closeprice,GKvolatility,(highPrice - lowPrice),(closeprice - openprice)])
result = pd.DataFrame(selectData,columns=["tradingDay", "updateTime", "bidprice", "bidvolume", "askprice", "askvolume",
                               "lastPrice", "tradevolume","tick_Vol", "openintrest","timesecond","Kindex","openPrice","highPrice","lowPrice","closePrice","GK"
                                          ,"xuti","shiti"])


pd.DataFrame.to_csv(result,"E:\\python_code\\tem_chen\\TA_data\\TA805#{0}.csv".format(instrument), index_label=False)
# 购买数据
