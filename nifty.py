import yfinance as yf
from datetime import date
import pandas as pd
import numpy as np

ticker='^NSEI'

ticker=yf.Ticker(ticker)

data=ticker.history(start=date(2014,1,1),end=date(2022,1,1))['Close']

data=data.resample('M').last()
fin=data[-1]/data[0]
data=np.log(data/data.shift(1)).dropna()


df=pd.DataFrame()
df['Portfolio']=['Nifty']
df['Mean']=np.mean(data)
df['Std']=np.std(data)
df['Fin Wealth']=fin
