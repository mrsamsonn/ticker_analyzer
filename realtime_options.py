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