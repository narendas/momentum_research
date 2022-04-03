import numpy as np
import pandas as pd

def get_data(stock):
    data=pd.read_csv('Historical Price Data/'+stock+'.csv')
    data['Date']=pd.to_datetime(data['Date'])
    data.index=data['Date']
    data.drop('Date',axis=1,inplace=True)    
    return data


def get_resampled_data(ticker,start,end,period):
    data=get_data(ticker)
    
    if period=='W':
        data['Returns']= data['Close'].pct_change()
        data['Log Returns']=np.log(data['Close']/data['Close'].shift(1)).dropna()
        vol=data['Log Returns'].resample('W').std()*np.sqrt(5)
    
    if period=='M':
        data['Returns']= data['Close'].pct_change()
        data['Log Returns']=np.log(data['Close']/data['Close'].shift(1)).dropna()
        vol=data['Log Returns'].resample('M').std()*np.sqrt(20)
    
    if period=='Y':
        data['Returns']= data['Close'].pct_change()
        data['Log Returns']=np.log(data['Close']/data['Close'].shift(1)).dropna()
        vol=data['Log Returns'].resample('Y').std()*np.sqrt(252)
    
    if period!='D':
        price_data=data[['Open','Close']].resample(period).last()
        
        volume_data=data[['Volume','Outstanding Shares']].resample(period).mean()
        
        data=pd.concat([price_data,volume_data],axis=1,join='inner')
    
    data['Returns']= data['Close'].pct_change()
    data['Log Returns']=np.log(data['Close']/data['Close'].shift(1)).dropna()
    
    
    data['Volume Change']=data['Volume'].pct_change()
    data['Log Volume Change']=np.log(data['Volume'].shift(1)/data['Volume']).dropna()
    
    data['Turnover Rate']=data['Volume']/data['Outstanding Shares']
    
    try:
        data['Volatility']=vol
        data['Inverse Volatility']=1/vol
    except:
        pass
    
    data['Unity']=1
    
    data.replace([np.inf, -np.inf], np.nan, inplace=True)
    data.dropna(inplace=True)
    return data