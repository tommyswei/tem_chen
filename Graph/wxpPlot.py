# encoding: utf-8
'''
@author: weixiang
@file: wxpPlot.py
@time: 2017/11/24 11:04
@desc:

绘图相关
'''

import numpy as np
import pandas as pd
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import seaborn as sns

def wxPlotRelix(dataCorr):
    """

    :param dataCorr: inpute  data.corr()
    :return:
    """

    corrdata=dataCorr
    # Set up the matplotlib figure
    f, ax = plt.subplots(figsize=(11, 9))

    sns.set(style="white")
    # Generate a mask for the upper triangle
    mask = np.zeros_like(corrdata, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True  # 显示对角线

    plt.rcParams['font.sans-serif'] = ["SimHei"]
    plt.rcParams['axes.unicode_minus'] = False

    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(220, 10, sep=10, n=2, center="light", as_cmap=True)

    # Draw the heatmap with the mask and correct aspect ratio
    sns.heatmap(corrdata, mask=mask, cmap=cmap, vmin=-1, vmax=1, center=0,
                square=True, linewidths=.5, cbar_kws={"shrink": .5})
    plt.show()
    plt.savefig(u"最终基金相关系数.png")



def wxScarterPlot(rawdata,datalist):
    """
    #  基金散点图，不同基金类型用不同的形状标识，并贮备基金名称

    :param rawdata:
    :param datalist:
    :return:
    """

    date = "2017-09-26"         # 画某天的散点图
    fig = plt.figure(figsize=(15, 10))
    ax1 = fig.add_subplot(111)
    plt.grid()
    plt.title(u"10只基金夏普比")

    # plt.plot()
    figure=["r>","rD","ro","bD","bo","b>","ko","k>","kD","yo","yD","y>"]

    i=0
    for instrument in datalist:

        returnnames=instrument+"_return"
        volatilityname=instrument+"_volatility"

        x=100*rawdata.loc[date][volatilityname]
        y=100*rawdata.loc[date][returnnames]
        print ("x is {0}; y is {1}".format(x,y))


        ax1.plot(100*x,100*y,figure[i],label=instrument)

        ax1.text(100*x,100*y+5,instrument,style='italic',bbox={'facecolor':'red', 'alpha':0.5, 'pad':10})

        i+=1
    ax1.set_xlabel(u'基金年化波动率')
    ax1.set_ylabel(u'基金年化收益率')
    plt.show()

def basic_plot(rawdata,):
    
    fig = plt.figure(figsize=(20, 12))
    ax1 = fig.add_subplot(111)
    plt.grid()
    plt.xticks(rotation=45)
    plt.yticks(rotation=45)
    ax1.plot(xline, highP, "r-")
    ax1.plot(xline, lowP, "c-")
    ax1.plot(xline, closeP, "g-")
    ax2 = ax1.twinx()
    ax2.plot(xline, GK, "k-")

    ax1.xaxis.set_major_locator(ticker.MaxNLocator(50))
    ax1.yaxis.set_major_locator(ticker.MaxNLocator(15))
    plt.show()
    


if __name__=="__main__":
    pass
