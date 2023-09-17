from yahoo_fin.stock_info import *

while get_live_price('SPY') != '':
    print(get_live_price('SPY'))