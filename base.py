import yfinance as yf
import numpy as np
import pandas as pd
import nsetools as nse
from nsepy import get_history
from datetime import date, timedelta

def get_data(ticker,start,end):
    ticker=yf.Ticker(ticker+'.NS')
    data=ticker.history( start=start, end=end)
    
    nifty_data=pd.read_csv('C:/Users/HP/Desktop/Repos/momentum_research/Nifty Historical Data.csv')
    
    nifty_2021=pd.read_csv('C:/Users/HP/Desktop/Repos/momentum_research/2021.csv')
    
    nifty_historical=nifty_data.append(nifty_2021).reset_index(drop=True)
    
    nifty_historical['Date']=pd.to_datetime(nifty_historical['Date'])
    nifty_historical.index=nifty_historical['Date']
    
    shares_traded=nifty_historical['Shares Traded']
    
    
    data=pd.concat([data,shares_traded],axis=1,join='inner')
    data['Outstanding Shares']=0
    
    data.loc[data.index[len(data)-1],'Outstanding Shares']=ticker.get_info()['sharesOutstanding']

    prev_index=data.index[len(data)-1]
    for index in data[:-1].index[::-1]:
        if data.loc[prev_index,'Stock Splits']!=0:
            data.loc[index,'Outstanding Shares']=data.loc[prev_index,'Outstanding Shares']/data.loc[prev_index,'Stock Splits']
        else:
            data.loc[index,'Outstanding Shares']=data.loc[prev_index,'Outstanding Shares']
        prev_index=index
        
    return data


def get_nse_data(ticker,start,end):
    data=get_history(ticker,start=start,end=end)
    data.index=pd.to_datetime(data.index)
    nifty_data=pd.read_csv('C:/Users/HP/Desktop/Repos/momentum_research/Nifty Historical Data.csv')
    
    nifty_2021=pd.read_csv('C:/Users/HP/Desktop/Repos/momentum_research/2021.csv')
    
    nifty_historical=nifty_data.append(nifty_2021).reset_index(drop=True)
    
    nifty_historical['Date']=pd.to_datetime(nifty_historical['Date'])
    nifty_historical.index=nifty_historical['Date']
    
    shares_traded=nifty_historical['Shares Traded']
    data['Outstanding Shares']=0
    
    
    ticker1=yf.Ticker(ticker+'.NS')
    
    stocksplit=ticker1.history(start=start,end=end)['Stock Splits']
    data=data.join(stocksplit,how='inner')
    data.loc[data.index[len(data)-1],'Outstanding Shares']=ticker1.get_info()['sharesOutstanding']
     
    prev_index=data.index[len(data)-1]
    for index in data[:-1].index[::-1]:
        if data.loc[prev_index,'Stock Splits']!=0:
            data.loc[index,'Outstanding Shares']=data.loc[prev_index,'Outstanding Shares']/data.loc[prev_index,'Stock Splits']
        else:
            data.loc[index,'Outstanding Shares']=data.loc[prev_index,'Outstanding Shares']
        prev_index=index
        
    data=pd.concat([data,shares_traded],axis=1,join='inner')        
    return data

def get_resampled_data(ticker,start,end,period):
    data=get_data(ticker,start=start,end=end)
    
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
        
        volume_data=data[['Volume','Shares Traded','Outstanding Shares']].resample(period).mean()
        
        data=pd.concat([price_data,volume_data],axis=1,join='inner')
    
    data['Returns']= data['Close'].pct_change()
    data['Log Returns']=np.log(data['Close']/data['Close'].shift(1)).dropna()
    
    
    data['Volume Change']=data['Volume'].pct_change()
    data['Log Volume Change']=np.log(data['Volume'].shift(1)/data['Volume']).dropna()
    
    data['Turnover Rate 1']=data['Volume']/data['Outstanding Shares']
    data['Inverse Turnover Rate 1']=data['Volume']/data['Outstanding Shares']
    
    data['Turnover Rate']=data['Volume']/data['Shares Traded']
    data['Inverse Turnover Rate']=1/data['Turnover Rate']
    
    try:
        data['Volatility']=vol
        data['Inverse Volatility']=1/vol
    except:
        pass
    
    data['Unity']=1
    
    data.replace([np.inf, -np.inf], np.nan, inplace=True)
    data.dropna(inplace=True)
    
    
    return data

def get_resampled_nse_data(ticker,start,end,period):
    data=get_nse_data(ticker,start=start,end=end)
    
    data['Returns']= data['Close'].pct_change()
    data['Log Returns']=np.log(data['Close']/data['Close'].shift(1)).dropna()
    data.index=pd.to_datetime(data.index)
    if period=='W':
        vol=data['Log Returns'].resample('W').std()*np.sqrt(5)
    
    if period=='M':
        vol=data['Log Returns'].resample('M').std()*np.sqrt(20)
    
    if period=='Y':
        vol=data['Log Returns'].resample('Y').std()*np.sqrt(252)
    
    price_data=data[['Open','Close']].resample(period).last()
    
    volume_data=data[['Volume','Shares Traded','Outstanding Shares']].resample(period).mean()
    
    data=pd.concat([price_data,volume_data],axis=1,join='inner')
    
    data['Returns']= data['Close'].pct_change()
    data['Log Returns']=np.log(data['Close']/data['Close'].shift(1)).dropna()
    
    
    data['Volume Change']=data['Volume'].pct_change()
    data['Log Volume Change']=np.log(data['Volume'].shift(1)/data['Volume']).dropna()
    
    
    data['Turnover Rate']=data['Volume']/data['Shares Traded']
    data['Inverse Turnover Rate']=1/data['Turnover Rate']
    
    data['Turnover Rate 1']=data['Volume']/data['Outstanding Shares']
    data['Inverse Turnover Rate 1']=data['Volume']/data['Outstanding Shares']
    
    data['Volatility']=vol
    data['Inverse Volatility']=1/vol
    
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

def strategy(investment,ins,outs):
    historical_returns=pd.DataFrame(columns=outs.columns,index=outs.index)
    historical_leftover=pd.DataFrame(columns=['BUY','SELL'],index=ins.index)
    capital_overtime=pd.DataFrame(columns=['Capital'],index=outs.index)
    
    for i in range(len(ins)):
        print(ins.index[i])
        market_entry=ins.loc[ins.index[i],:]
        
        capital_entry=market_entry*investment
        
        capital_entry=capital_entry[capital_entry!=0]
        capital_entry=(-1)*capital_entry
        stocks_entry=capital_entry.copy()
        
        capital_exit=stocks_entry.copy()
        
        buy_capital=0
        sell_capital=0
        for index in capital_entry.index:
            capital=(-1)*capital_entry[index]
            stock_data=get_history(index,start=ins.index[i],end=outs.index[i])
            if len(stock_data)>0:
                entry_stock_price=stock_data['Open'][0]
                
                no_of_stocks=capital/entry_stock_price
                no_of_stocks=no_of_stocks
                
                stocks_entry[index]=no_of_stocks
                
                if capital>0:
                    buy_capital+=-no_of_stocks*entry_stock_price
                
                if capital<0:
                    sell_capital+=-no_of_stocks*entry_stock_price
                
                exit_stock_price=stock_data['Close'][-1]
                capital_exit[index]=exit_stock_price*no_of_stocks*(-1)
                
                capital_entry[index]=no_of_stocks*entry_stock_price
            else:
                capital_entry[index]=0
                capital_exit[index]=0
                
        historical_leftover.loc[ins.index[i],'BUY']=buy_capital
        historical_leftover.loc[ins.index[i],'SELL']=sell_capital
        returns=capital_exit+capital_entry
        historical_returns.loc[outs.index[i],returns.index]=returns
        
        investment=investment+returns.sum()
        
        capital_overtime.loc[outs.index[i],'Capital']=investment
    return historical_returns,historical_leftover,capital_overtime

def sell_strategy(investment,ins,outs):
    historical_returns=pd.DataFrame(columns=outs.columns,index=outs.index)
    
    for i in range(len(ins)):
        print(ins.index[i])
        market_entry=ins.loc[ins.index[i],:]
        
        capital_entry=market_entry*investment
        
        capital_entry=capital_entry[capital_entry!=0]
        capital_entry=(-1)*capital_entry
        
        capital_returns=capital_entry.copy()
        
        sell_capital=0
        for index in capital_entry.index:
            capital=capital_entry[index]
            ticker=yf.Ticker(index+'.NS')
            stock_data=ticker.history(start=ins.index[i],end=outs.index[i])
            
            returns=0
            for j in stock_data.index:
                no_of_stocks=capital/stock_data.loc[j,'Open']
                
                bought_back=no_of_stocks*stock_data.loc[j,'Close']
                
                returns+=capital-bought_back
                capital=bought_back
            capital_returns[index]=returns
            
        #short_returns=capital_returns.sum()
        historical_returns.loc[outs.index[i],capital_returns.index]=capital_returns
        
        
    return historical_returns