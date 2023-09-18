# from yahoo_fin.stock_info import *
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
#import ta_py as ta
import numpy as np
import talib as ta

# while get_live_price('SPY') != '':
#     print(get_live_price('SPY'))

#################
#test static analysis first

#vars
data = yf.download('SPY')
data['ema50'] = ta.EMA(data["Adj Close"], 50) 
data['ema200'] = ta.EMA(data["Adj Close"], 200)
data['crossing'] = 0
data['ema_winrate'] = 0

def percent_change(df, i):  #(new_price-old_price)/old_price *100
     return ((df.iloc[i]-df.iloc[i-1])/df.iloc[i-1])*100

#plots winrate from price, 2 inputs
def winrate_plotter(df_price, df_crossing, df_in_1, df_in_2, df_winrate):
    winrate = 0
    for i in range(len(df_price)):
        if df_in_1.iloc[i] >= df_in_2.iloc[i]:
            df_crossing.iloc[i] = 10
            if percent_change(df_price,i) >= 5:       #+5%
                winrate=winrate+1
                df_winrate.iloc[i]=20
        if percent_change(df_price,i) <= -5:       #-5%
                winrate=winrate+1
                df_winrate.iloc[i]=20
    return winrate, df_winrate

ema_winrate, data['ema_winrate'] = winrate_plotter(data['Adj Close'], data['crossing'], data['ema50'], data['ema200'], data['ema_winrate'])

print(data)
print('ema_winrate:',ema_winrate ,'/',len(data))

plt.plot(data.index, data['Adj Close'], label='Closing Price')
plt.plot(data.index,data['ema50'], label='EMA_50')
plt.plot(data.index,data['ema200'], label='EMA_200')
plt.plot(data.index,data['crossing'], label='EMA_50/200_Crossing')
plt.plot(data.index,data['ema_winrate'], label='ema_wins +-5% price change', color='cyan')
plt.legend(loc="upper left")
plt.show()
