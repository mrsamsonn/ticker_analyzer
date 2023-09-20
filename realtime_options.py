import os
import sys
import pickle
import numpy as np
import pandas as pd

from datetime import timedelta, datetime, date
from thetadata import ThetaClient, OptionReqType, OptionRight, DateRange, DataType, StockReqType
from thetadata import MessageType, TradeCondition
from thetadata import StreamMsg, StreamMsgType

#temp-login thetadata
your_username = os.environ['fimep87646@utwoko.com']
your_password = os.environ['ticker_analyzer']

# User generated method that gets called each time a message from the stream arrives.
def callback(msg: StreamMsg):
    msg.type = msg.type

    if msg.type == StreamMsgType.TRADE:
        print('---------------------------------------------------------------------------')
        print('con:                         ' + msg.contract.to_string())
        print('trade:                       ' + msg.trade.to_string())
        print('last quote at time of trade: ' + msg.quote.to_string())

client = ThetaClient(username=your_username, passwd=your_password)
client.connect_stream(callback)
client.req_full_trade_stream_opt()  # Subscribes to every option trade.

client.remove_full_trade_stream_opt()  # Unsubscribes from the full option trade stream.
client.close_stream()

def get_expirations(root_ticker) -> pd.DataFrame:
    """Request expirations from a particular options root"""
    # Create a ThetaClient
    client = ThetaClient(username=your_username, passwd=your_password, jvm_mem=4, timeout=15)

    # Connect to the Terminal
    with client.connect():

        # Make the request
        data = client.get_expirations(
            root=root_ticker,
        )

    return data

root_ticker = 'AMZN'
expirations = get_expirations(root_ticker)
expirations

trading_days = pd.date_range(start=datetime(2023,1,24),end=datetime(2024,12,31),freq='B')
# The third friday in every month
contracts = pd.date_range(start=datetime(2023,1,24),end=datetime(2024,12,31),freq='WOM-3FRI')
# Find contract expiries that match with ThetaData expiries 
mth_expirations = [exp for exp in expirations if exp in contracts]
# Convert from python list to pandas datetime
mth_expirations = pd.to_datetime(pd.Series(mth_expirations))

mth_expirations


def get_strikes(root_ticker, expiration_dates) -> pd.DataFrame:
    """Request strikes from a particular option contract"""
    # Create a ThetaClient
    client = ThetaClient(username=your_username, passwd=your_password, jvm_mem=4, timeout=15)
    
    all_strikes = {}

    # Connect to the Terminal
    with client.connect():
        
        for exp_date in expiration_dates:
        
            # Make the request
            data = client.get_strikes(
                root=root_ticker,
                exp=exp_date
            )
            
            all_strikes[exp_date] = pd.to_numeric(data)
            

    return all_strikes


root_ticker = 'AMZN'

all_strikes = get_strikes(root_ticker, mth_expirations)

with open('strikes.pkl', 'wb') as f:
    pickle.dump(all_strikes, f)


with open('strikes.pkl', 'rb') as f:
    all_strikes = pickle.load(f)
    
print("Option Contract: ", mth_expirations[0])
print("AMZN Strike ", all_strikes[mth_expirations[0]][13])

######################
#REAL TIME
######################

client = ThetaClient(username=your_username, passwd=your_password)
client.connect_stream(callback)

root_ticker = 'AMZN'
opt_types=["P", "C"]
for opt_type in opt_types:
    for expiry in mth_expirations:
        strikes = all_strikes[expiry]
        for strike in strikes:
            # add specific contract to required trade stream using req_trade_stream_opt()
            client.req_trade_stream_opt(root_ticker, expiry.date(), strike, OptionRight.CALL if opt_type=="C" else OptionRight.PUT)

