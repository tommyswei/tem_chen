# -*- coding: utf-8 -*-
"""
@ Time    : 2018-03-28 22:53
@ author  : weixiang
@ FileName: basic_plot.py
@ User    : 魏翔
@ desc    :

"""
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
from tool_packages.wx_talib import *

rad =pd.read_csv("E:\\python_code\\tem_chen\\TA_data\\TA805#20180327.csv",header=0)
rad_min =pd.read_csv("E:\\python_code\\tem_chen\\TA_data\\TA805#20180327_min.csv",header=0)

s = RSI(rad_min, 3)
rad_min.tail()
rad_min.head()

# rad_min = rad_min.reset_index("timesecond")



plt.grid()
plt.xticks(rotation=45)
plt.yticks(rotation=45)
xline = []
lastP =[]
rsi3 = []
rsi3_x = []

result = []
for item in rad.index:
    # item = rad.index[3]
    # xline.append(item)
    # lastP.append(rad.loc[item,"lastPrice"])
    tem_rsi = 0
    tem_index = rad.loc[item,"Kindex"]
    min_point = rad_min[rad_min["Kindex"]==tem_index].index
    # if min_point in rad_min["min_point"]:
    tem_data = rad_min.loc[min_point,"rsi_3"]
    if len(tem_data)>=1 :
        tem_rsi = rad_min.loc[min_point,"rsi_3"].values[0]
    # else:
    #     print("{0} and {1} ".format(tem_index,min_point))
    if tem_rsi == np.nan:
        result.append(0)
    else:
        result.append(tem_rsi)

len(result)
len(rad)
rad["rsi_3_1min"] = result


fig = plt.figure(figsize=(20, 12))
plt.title("PTA 2018#03#28 tick & rsi")
ax1 = fig.add_subplot(111)
# ax2 = fig.add_subplot(212)
ax1.plot( rad["lastPrice"], "k-",label = "tick lastP")
plt.legend()
ax2=ax1.twinx()
ax2.plot(rad["rsi_3_1min"], "c-",label ="1 min RSI")
plt.legend()
# ax1.plot(xline, closeP, "g-")
# ax2.plot(rad["GK"],"r-")
# ax1.grid()
ax1.xaxis.set_major_locator(ticker.MaxNLocator(50))
ax1.yaxis.set_major_locator(ticker.MaxNLocator(15))
# ax2.xaxis.set_major_locator(ticker.MaxNLocator(50))
# ax2.yaxis.set_major_locator(ticker.MaxNLocator(15))
plt.show()