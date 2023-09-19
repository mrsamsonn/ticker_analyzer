# from yahoo_fin.stock_info import *
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
#import ta_py as ta
import numpy as np
import talib as ta

# while get_live_price('SPY') != '':
#     print(get_live_price('SPY'))

###########################################
########test static analysis first#########
###########################################

##############################
#function declarations
def percent_change(df, i):  #(new_price-old_price)/old_price *100
     return ((df.iloc[i]-df.iloc[i-1])/df.iloc[i-1])*100

################################

#vars
data = yf.download('SPY')
data['ema50'] = ta.EMA(data["Adj Close"], 50) 
data['ema200'] = ta.EMA(data["Adj Close"], 200)
data['macd'], data['macdsignal'], data['macdhist'] = ta.MACD(data["Adj Close"], 12, 26, 9)
data['ema_crossing'] = 0
data['ema_entry'] = 0
data['ema_close'] = 0
data['ema_total'] = 0
data['ema_winrate'] = 0
data['macd_winrate'] = 0

#EMA crossover
ema_winrate = 0
for i in range(len(data)):
    if data['ema50'].iloc[i] >= data['ema200'].iloc[i] and data['ema50'].iloc[i-1] <= data['ema200'].iloc[i-1]:
        data['ema_crossing'].iloc[i] = 10
        if percent_change(data["Adj Close"],i) >= 5:       #+5%
            ema_winrate=ema_winrate+1
            data['ema_winrate'].iloc[i]=20
    else:
        if percent_change(data["Adj Close"],i) <= -5:       #-5%
                ema_winrate=ema_winrate+1
                data['ema_winrate'].iloc[i]=20

#EMA entry calc
for i in range(len(data)):
    if data['ema_crossing'].iloc[i] == 0:
        #entry
        data['ema_entry'].iloc[i] = data['Adj Close'].iloc[i]
    else:
        data['ema_close'].iloc[i] = data['Adj Close'].iloc[i]
        data['ema_total'].iloc[i] = data['ema_close'].iloc[i] - data['ema_entry'].iloc[i]

#MACD histogram
macd_winrate = 0
for i in range(len(data)):
    if data['macdhist'].iloc[i] >= 0:
        if percent_change(data['Adj Close'],i) >= 5:
            macd_winrate=macd_winrate+1
            data['macd_winrate'].iloc[i]=30
    else:
         if percent_change(data['Adj Close'],i) <= -5:
            macd_winrate=macd_winrate+1
            data['macd_winrate'].iloc[i]=30
     
             
#####Terminal Outputs
print(data)
print('ema_winrate:',ema_winrate ,'/',len(data),'=',round(((ema_winrate/len(data))*100),2),'%')
print('macd_winrate:',macd_winrate ,'/',len(data),'=',round(((macd_winrate/len(data))*100),2),'%')


#####Plots
figure, axis = plt.subplots(3)
axis[0].title.set_text('SPY500')
axis[0].plot(data.index, data['Adj Close'], label='Closing Price')
axis[0].plot(data.index,data['ema50'], label='EMA_50')
axis[0].plot(data.index,data['ema200'], label='EMA_200')
axis[0].plot(data.index,data['macd_winrate'], label='macd_wins +-5% price change', color='pink')
#axis[0].plot(data.index,data['ema_crossing'], label='EMA_50/200_Crossing')
axis[0].plot(data.index,data['ema_winrate'], label='ema_wins +-5% price change', color='cyan')
axis[0].legend(loc="upper left")

# axis[1].plot(data.index,data['macd'], label='macd')
# axis[1].plot(data.index,data['macdsignal'], label='macdsignal')
colors = ['g' if i >= 0 else 'r' for i in data['macdhist']] #for histogram color : red if < 0, green if > 0
axis[1].bar(data.index, data['macdhist'], label='macdhist', color=colors)
axis[1].legend(loc="upper left")

axis[2].plot(data.index, data['ema_total'], label='ema_total')
axis[2].legend(loc="upper left")
plt.title('SPY500')
plt.show()
