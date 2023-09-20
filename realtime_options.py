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