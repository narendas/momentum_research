import os
os.chdir(r'C:/Users/HP/Desktop/Repos/momentum_research')
import yfinance as yf
import numpy as np
import pandas as pd
from base import get_data, get_resampled_data,get_nse_data, get_resampled_nse_data

from datetime import date

stock='RPOWER'

mass='Inverse Turnover Rate'
velocity='Log Returns'


ticker=yf.Ticker(stock+'.NS')
data=get_data(ticker,start='2015-01-01')
resampled_data=get_resampled_data(ticker, start='2015-01-01', period='W')


nse_data=get_nse_data(stock,start=date(2015,1,1),end=date(2021,12,2))
resampled_nse_data=get_resampled_nse_data(stock, start=date(2015,1,1), end=date(2021,11,30), period='W')
momentum=resampled_nse_data[mass]*resampled_nse_data[velocity]
