from tvDatafeed import TvDatafeed, Interval
import matplotlib.pyplot as plt

tv = TvDatafeed()

nifty_index_data = tv.get_hist(symbol='NIFTY',exchange='NSE',interval=Interval.in_1_hour,n_bars=1000)

print(nifty_index_data)
nifty_index_data.reset_index(inplace=True)
nifty_index_data.plot(x='datetime', y='close')
plt.show()