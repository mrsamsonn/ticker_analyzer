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

data = yf.download('SPY')
data['ema50'] = ta.EMA(data["Adj Close"], 50) 
data['ema200'] = ta.EMA(data["Adj Close"], 200)
data['crossing'] = 0


i=0
while i != len(data):
    if data['ema50'].iloc[i] >= data['ema200'].iloc[i]:
        data['crossing'].iloc[i] = 10
    i=i+1


    

print(data)


plt.plot(data.index, data['Adj Close'], label='Closing Price')
plt.plot(data.index,data['ema50'], label='EMA_50')
plt.plot(data.index,data['ema200'], label='EMA_200')
plt.plot(data.index,data['crossing'], label='EMA_50/200_Crossing')
plt.legend(loc="upper left")
plt.show()
