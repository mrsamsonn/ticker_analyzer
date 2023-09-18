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

print(data)


plt.plot(data.index, data['Adj Close'])
plt.plot(data.index,data['ema50'])
plt.plot(data.index,data['ema200'])
plt.show()
