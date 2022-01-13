import yfinance as yf
import numpy as np

ticker=yf.Ticker('INFY.NS')


data=ticker.history(start='2019-01-01')

data['Outstanding Shares']=0

data.loc[data.index[len(data)-1],'Outstanding Shares']=ticker.get_info()['sharesOutstanding']

prev_index=data.index[len(data)-1]
for index in data[:-1].index[::-1]:
    if data.loc[prev_index,'Stock Splits']!=0:
        data.loc[index,'Outstanding Shares']=data.loc[prev_index,'Outstanding Shares']/data.loc[prev_index,'Stock Splits']
    else:
        data.loc[index,'Outstanding Shares']=data.loc[prev_index,'Outstanding Shares']
    prev_index=index

data['Turnover Rate']=data['Volume']/data['Outstanding Shares']


data['Volume MA']=data['Volume'].rolling(100).mean()

data['Volume Ratio']=data['Volume']/data['Volume MA']

#data['Returns']= data['Close'].pct_change()
data['Returns']=np.log(data['Close']/data['Close'].shift(1)).dropna()
data.replace([np.inf, -np.inf], np.nan, inplace=True)
data.dropna(inplace=True)

print(np.corrcoef(data['Returns'],data['Turnover Rate']))
