# from yahoo_fin.stock_info import *
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

# while get_live_price('SPY') != '':
#     print(get_live_price('SPY'))

#################
#test static analysis first

data = yf.download('SPY')
print(data)


plt.plot(data.index, data['Adj Close'])
plt.show()

