import yfinance as yf
import numpy as np
import pandas as pd
import nsetools as nse
from nsepy import get_history
from datetime import date, timedelta

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

def sampling(data,iterations,sample_size):
    sampling_data=[]
    for i in range(iterations):
        sample=np.random.choice(data,sample_size, replace=True)
        sampling_data.append(sample.mean())
    
    return np.array(sampling_data)

def sampling_corr(data,mass,velocity,iterations,sample_size):
    sampling_data=[]
    for i in range(iterations):
        sample=data.sample(sample_size,replace=True)
        corr=np.corrcoef(sample[mass],sample[velocity])[0,1]
        
        sampling_data.append(corr)
    return np.array(sampling_data)


def get_all_stocks():
    df=pd.read_csv('C:/Users/HP/Desktop/Repos/momentum_research/nifty_companies.csv')
    
    stocks_list=[]
    for column in df.columns:
        stocks=df[column]
        
        append_list=[element for element in stocks if element not in stocks_list]
        
        stocks_list.extend(append_list)
    return stocks_list

def momentum_matrix(mass,velocity,resample,start,end):
    stocks=get_all_stocks()
    momentum_matrix=pd.DataFrame()
    for stock in stocks:
        print(stock)
        try:
            resampled_data=get_resampled_data(stock,start=start,end=end,period=resample)
            momentum=resampled_data[mass]*resampled_data[velocity]  
            momentum_matrix[stock]=momentum
        except:
            pass
    return momentum_matrix

def mass(mass,resample):
    stocks=get_all_stocks()
    momentum_matrix=pd.DataFrame()
    for stock in stocks:
        print(stock)
        try:
            resampled_data=get_resampled_data(stock,start=date(2015,1,1),end=date(2021,11,30),period=resample)
        except:
            pass
        momentum=resampled_data[mass]
        momentum_matrix[stock]=momentum
    return momentum_matrix

def momentum_1(matrix,j,k,equal=True,contrarian=False):
    prev_comb=''
    ins=pd.DataFrame(columns=matrix.columns,index=matrix.index[j-1:-k])
    outs=pd.DataFrame(columns=matrix.columns,index=matrix.index[j-1+k:])
    for i in range(j-1,len(matrix.index)-k):
        year=str(matrix.index[i].year)[2:]
        month=str(matrix.index[i].month_name())[:3]
        
        comb=month+'-'+year
        
        lookback1=matrix[i+1-j:i+1]
        holding1=matrix[i+1:i+k+1]
        
        nifty_companies=pd.read_csv('C:/Users/HP/Desktop/Repos/momentum_research/nifty_companies.csv')
        
        if prev_comb!=comb:
            companies=list(nifty_companies[comb])
            
        prev_comb=comb
        
        companies=[company for company in companies if company in matrix.columns]
        lookback=lookback1[companies]
        holding=holding1[companies]
        
        momentum=lookback.sum()
        
        positive_momentum=momentum[momentum>0]
        positive_rank=positive_momentum.rank(pct=True)
        
        buy_companies=positive_rank[positive_rank>=0.9].index
        
        if len(buy_companies)>0:
            if equal==True:
                buy_weights=pd.Series(1/len(buy_companies),index=buy_companies)
            
            else:
                buy_weights=pd.Series(index=buy_companies)
                buy_weights=positive_momentum[buy_weights.index]
                
                buy_weights=buy_weights/buy_weights.sum()
            
            buy_weights=buy_weights
            for company in buy_companies:
                ins.loc[matrix.index[i],company]=-1*buy_weights[buy_weights.index==company][0]
                
        
        negative_momentum=momentum[momentum<0]
        negative_rank=negative_momentum.rank(pct=True)
        sell_companies=negative_rank[negative_rank>=0.9].index
        
        if len(sell_companies)>0:
            if equal==True:
                sell_weights=pd.Series(-1/len(sell_companies),index=sell_companies)
            else:
                sell_weights=pd.Series(index=sell_companies)
                sell_weights=negative_momentum[sell_weights.index]
                
                sell_weights=-sell_weights/sell_weights.sum()
            
            sell_weights=sell_weights
            for company in sell_companies:
                ins.loc[matrix.index[i],company]=0*sell_weights[sell_weights.index==company][0]
        
# =============================================================================
#         if len(sell_companies)>0 and len(buy_companies)>0:
#             ins.loc[matrix.index[i],:]=ins.loc[matrix.index[i],:]*0.5
# =============================================================================
    
    outs=pd.DataFrame(-np.array(ins),index=outs.index,columns=outs.columns)
    
    ins.fillna(0,inplace=True)
    outs.fillna(0,inplace=True)
    
    ins.index=ins.index+timedelta(days=1)
    
    if contrarian==True:
        ins=-ins
        outs=-outs
    return ins,outs


def momentum_2(matrix,mass,j,k,equal=True,contrarian=False):
    prev_comb=''
    ins=pd.DataFrame(columns=matrix.columns,index=matrix.index[j-1:-k])
    outs=pd.DataFrame(columns=matrix.columns,index=matrix.index[j-1+k:])
    
    for i in range(j-1,len(matrix.index)-k):
        year=str(matrix.index[i].year)[2:]
        month=str(matrix.index[i].month_name())[:3]
        
        comb=month+'-'+year
        
        lookback=matrix[i+1-j:i+1]
        holding=matrix[i+1:i+k+1]
        
        lookback_mass=mass[i+1-j:i+1]
        holding_mass=mass[i+1:i+k+1]
        nifty_companies=pd.read_csv('C:/Users/HP/Desktop/Repos/momentum_research/nifty_companies.csv')
        
        if prev_comb!=comb:
            companies=list(nifty_companies[comb])
            
        prev_comb=comb
        
        lookback=lookback[companies]
        holding=holding[companies]
        
        lookback_mass=lookback_mass[companies]
        holding_mass=holding_mass[companies]
        
        lookback=lookback.dropna(axis=1)
        holding=holding.dropna(axis=1)
        lookback_mass=lookback_mass.dropna(axis=1)
        holding_mass=holding_mass.dropna(axis=1)
        
        momentum=lookback.sum()/lookback_mass.sum()
        
        positive_momentum=momentum[momentum>0]
        positive_rank=positive_momentum.rank(pct=True)
        
        buy_companies=positive_rank[positive_rank>=0.9].index
        
        if len(buy_companies)>0:
            if equal==True:
                buy_weights=pd.Series(1/len(buy_companies),index=buy_companies)
            
            else:
                buy_weights=pd.Series(index=buy_companies)
                buy_weights=positive_momentum[buy_weights.index]
                
                buy_weights=buy_weights/buy_weights.sum()
            
            buy_weights=buy_weights*0.5
            for company in buy_companies:
                ins.loc[matrix.index[i],company]=-1*buy_weights[buy_weights.index==company][0]
                
        
        negative_momentum=momentum[momentum<0]
        negative_rank=negative_momentum.rank(pct=True)
        sell_companies=negative_rank[negative_rank<=0.1].index
        
        if len(sell_companies)>0:
            if equal==True:
                sell_weights=pd.Series(-1/len(sell_companies),index=sell_companies)
            else:
                sell_weights=pd.Series(index=sell_companies)
                sell_weights=negative_momentum[sell_weights.index]
                
                sell_weights=-sell_weights/sell_weights.sum()
            
            sell_weights=sell_weights*0
            for company in sell_companies:
                ins.loc[matrix.index[i],company]=sell_weights[sell_weights.index==company][0]
        
    
    outs=pd.DataFrame(-np.array(ins),index=outs.index,columns=outs.columns)
    
    ins.fillna(0,inplace=True)
    outs.fillna(0,inplace=True)
    
    ins.index=ins.index+timedelta(days=1)
    
    if contrarian==True:
        ins=-ins
        outs=-outs
    return ins,outs

def momentum_3(matrix,j,k,equal=True,contrarian=False):    
    prev_comb=''
    ins=pd.DataFrame(columns=matrix.columns,index=matrix.index[j-1:-k])
    outs=pd.DataFrame(columns=matrix.columns,index=matrix.index[j-1+k:])
    
    for i in range(j-1,len(matrix.index)-k):
        year=str(matrix.index[i].year)[2:]
        month=str(matrix.index[i].month_name())[:3]
        
        comb=month+'-'+year
        
        lookback=matrix[i+1-j:i+1]
        holding=matrix[i+1:i+k+1]
        
        nifty_companies=pd.read_csv('C:/Users/HP/Desktop/Repos/momentum_research/nifty_companies.csv')
        
        if prev_comb!=comb:
            companies=list(nifty_companies[comb])
            
        prev_comb=comb
        
        lookback=lookback[companies]
        holding=holding[companies]
        
        lookback=lookback.dropna(axis=1)
        holding=holding.dropna(axis=1)
        
        momentum=lookback.mean()/lookback.std()
        
        positive_momentum=momentum[momentum>0]
        positive_rank=positive_momentum.rank(pct=True)
        
        buy_companies=positive_rank[positive_rank>=0.9].index
        
        if len(buy_companies)>0:
            if equal==True:
                buy_weights=pd.Series(1/len(buy_companies),index=buy_companies)
            
            else:
                buy_weights=pd.Series(index=buy_companies)
                buy_weights=positive_momentum[buy_weights.index]
                
                buy_weights=buy_weights/buy_weights.sum()
            
            buy_weights=buy_weights*0.5
            for company in buy_companies:
                ins.loc[matrix.index[i],company]=-1*buy_weights[buy_weights.index==company][0]
                
        
        negative_momentum=momentum[momentum<0]
        negative_rank=negative_momentum.rank(pct=True)
        sell_companies=negative_rank[negative_rank<=0.1].index
        
        if len(sell_companies)>0:
            if equal==True:
                sell_weights=pd.Series(-1/len(sell_companies),index=sell_companies)
            else:
                sell_weights=pd.Series(index=sell_companies)
                sell_weights=negative_momentum[sell_weights.index]
                
                sell_weights=-sell_weights/sell_weights.sum()
            
            sell_weights=sell_weights*0.5
            for company in sell_companies:
                ins.loc[matrix.index[i],company]=sell_weights[sell_weights.index==company][0]
        
    
    outs=pd.DataFrame(-np.array(ins),index=outs.index,columns=outs.columns)
    
    ins.fillna(0,inplace=True)
    outs.fillna(0,inplace=True)
    
    ins.index=ins.index+timedelta(days=1)
    
    if contrarian==True:
        ins=-ins
        outs=-outs
    return ins,outs