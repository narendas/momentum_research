import os
os.chdir(r'C:/Users/HP/Desktop/Repos/momentum_research')
import numpy as np
import pandas as pd
from base import get_all_stocks,get_resampled_data
from datetime import date,timedelta
from nsepy import get_history
import yfinance as yf
import matplotlib.pyplot as plt

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

def mass(mass,resample,start,end):
    stocks=get_all_stocks()
    momentum_matrix=pd.DataFrame()
    for stock in stocks:
        print(stock)
        try:
            resampled_data=get_resampled_data(stock,start=start,end=end,period=resample)
        except:
            pass
        momentum=resampled_data[mass]
        momentum_matrix[stock]=momentum
    return momentum_matrix

def momentum_day_1(matrix,j,k,equal=True,contrarian=False):
    prev_comb=''
    ins=pd.DataFrame(columns=matrix.columns,index=matrix.index[j:])
    outs=pd.DataFrame(columns=matrix.columns,index=matrix.index[j:])
    for i in range(j,len(matrix.index)):
        year=str(matrix.index[i].year)[2:]
        month=str(matrix.index[i].month_name())[:3]
        
        comb=month+'-'+year
        
        lookback1=matrix[i-j:i]
        holding1=matrix[i:i+k]
        
        nifty_companies=pd.read_csv('C:/Users/HP/Desktop/Repos/momentum_research/nifty_companies.csv')
        
        if prev_comb!=comb:
            companies=list(nifty_companies[comb])
         
        companies=[company for company in companies if company in matrix.columns]
        prev_comb=comb
        
        lookback=lookback1[companies]
        holding=holding1[companies]
        
        momentum=lookback.sum()
        
        positive_momentum=momentum[momentum>=max(momentum)]
        positive_rank=positive_momentum.rank(pct=True)
        
        buy_companies=positive_rank[positive_rank>=0].index
        
        if len(buy_companies)>0:
            if equal==True:
                buy_weights=pd.Series(1/len(buy_companies),index=buy_companies)
            
            else:
                buy_weights=pd.Series(index=buy_companies)
                buy_weights=positive_momentum[buy_weights.index]
                
                buy_weights=buy_weights/buy_weights.sum()
            
            buy_weights=buy_weights
            for company in buy_companies:
                ins.loc[matrix.index[i],company]=0*buy_weights[buy_weights.index==company][0]
                
        
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
                ins.loc[matrix.index[i],company]=sell_weights[sell_weights.index==company][0]
        
    outs=pd.DataFrame(-np.array(ins),index=outs.index,columns=outs.columns)
    
    ins.fillna(0,inplace=True)
    outs.fillna(0,inplace=True)
        
    if contrarian==True:
        ins=-ins
        outs=-outs
    return ins,outs

def momentum_day_2(matrix,mass,j,k,equal=True,contrarian=False):
    prev_comb=''
    ins=pd.DataFrame(columns=matrix.columns,index=matrix.index[j:])
    outs=pd.DataFrame(columns=matrix.columns,index=matrix.index[j:])
    for i in range(j,len(matrix.index)):
        year=str(matrix.index[i].year)[2:]
        month=str(matrix.index[i].month_name())[:3]
        
        comb=month+'-'+year
        
        lookback1=matrix[i-j:i]
        holding1=matrix[i:i+k]
        
        lookback_mass=mass[i+1-j:i+1]
        holding_mass=mass[i+1:i+k+1]
        
        nifty_companies=pd.read_csv('C:/Users/HP/Desktop/Repos/momentum_research/nifty_companies.csv')
        
        if prev_comb!=comb:
            companies=list(nifty_companies[comb])
         
        companies=[company for company in companies if company in matrix.columns]
        prev_comb=comb
        
        lookback=lookback1[companies]
        holding=holding1[companies]
        
        lookback_mass=lookback_mass[companies]
        holding_mass=holding_mass[companies]
        
        lookback=lookback.dropna(axis=1)
        holding=holding.dropna(axis=1)
        lookback_mass=lookback_mass.dropna(axis=1)
        holding_mass=holding_mass.dropna(axis=1)
        
        momentum=lookback.sum()/lookback_mass.sum()
        
        positive_momentum=momentum[momentum>=max(momentum)]
        positive_rank=positive_momentum.rank(pct=True)
        
        buy_companies=positive_rank[positive_rank>=0].index
        
        if len(buy_companies)>0:
            if equal==True:
                buy_weights=pd.Series(1/len(buy_companies),index=buy_companies)
            
            else:
                buy_weights=pd.Series(index=buy_companies)
                buy_weights=positive_momentum[buy_weights.index]
                
                buy_weights=buy_weights/buy_weights.sum()
            
            buy_weights=buy_weights
            for company in buy_companies:
                ins.loc[matrix.index[i],company]=0*buy_weights[buy_weights.index==company][0]
                
        
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
                ins.loc[matrix.index[i],company]=sell_weights[sell_weights.index==company][0]
        
    outs=pd.DataFrame(-np.array(ins),index=outs.index,columns=outs.columns)
    
    ins.fillna(0,inplace=True)
    outs.fillna(0,inplace=True)
        
    if contrarian==True:
        ins=-ins
        outs=-outs
    return ins,outs

def portfolio_value(ins,outs,investment,k):
    capital_history=pd.DataFrame(index=ins.index,columns=['Capital'])
    capital_history.loc[ins.index[:k],'Capital']=investment
    capital_history.loc[ins.index[-1]+timedelta(days=1),'Capital']=0
    for i in range(len(ins.index)):
        print(ins.index[i])
        market_entry=ins.loc[ins.index[i],:]
        investment=capital_history.loc[ins.index[i],'Capital']
        capital_entry=market_entry*investment
        capital_entry=capital_entry[capital_entry!=0]
        
        capital_entry=-1*capital_entry
        
        total_returns=0
        for company in capital_entry.index:
            capital=capital_entry[company]
            
            ticker=yf.Ticker(company+'.NS')
            stock_data=ticker.history(start=ins.index[i],end=outs.index[i]+timedelta(days=1))
            
            if len(stock_data)<0:
                break
            no_of_stock=capital/stock_data['Open'][0]
            
            buy_back=no_of_stock*stock_data['Close'][0]
            
            capital=capital+(capital-buy_back)
            
            returns=capital-capital_entry[company]
            total_returns+=returns
        
        capital_history.loc[capital_history.index[i+1],'Capital']=investment+total_returns
    return capital_history

def portfolio_long_value(ins,outs,investment,k):
    capital_history=pd.DataFrame(index=ins.index,columns=['Capital'])
    capital_history.loc[ins.index[:k],'Capital']=investment
    capital_history.loc[ins.index[-1]+timedelta(days=1),'Capital']=0
    for i in range(len(ins.index)):
        print(ins.index[i])
        market_entry=ins.loc[ins.index[i],:]
        investment=capital_history.loc[ins.index[i],'Capital']
        capital_entry=market_entry*investment
        capital_entry=capital_entry[capital_entry!=0]
        
        capital_entry=capital_entry
        
        total_returns=0
        for company in capital_entry.index:
            capital=capital_entry[company]
            
            ticker=yf.Ticker(company+'.NS')
            stock_data=ticker.history(start=ins.index[i],end=outs.index[i]+timedelta(days=1))
                        
            no_of_stock=capital/stock_data['Open'][0]
            
            buy_back=no_of_stock*stock_data['Close'][0]
            
            returns=buy_back-capital
            total_returns+=returns
        
        capital_history.loc[capital_history.index[i+1],'Capital']=investment+total_returns
    return capital_history

ticker='^NSEI'
ticker=yf.Ticker(ticker)
data=ticker.history(start=date(2015,1,1),end=date(2021,11,30))
matrix=momentum_matrix('Inverse Turnover Rate 1','Log Returns','D',start=date(2015,1,1),end=date(2021,11,30))
for j in range(4,8):
    for k in range(1,2):
        if k<=j:
            ins,outs=momentum_day_1(matrix,j=j,k=k,equal=False,contrarian=False)
            port_value=portfolio_value(ins,outs,8000,k=k)
            port_value.plot()
            port_value.to_csv('Shorting/momentum_1/Inverse Turnover Rate 1/'+str(j)+str(k)+'.csv')
            data['Close'].plot()
            plt.show()

#mass=mass('Turnover Rate 1','D',start=date(2015,1,1),end=date(2021,11,30))
for j in range(2,8):
    for k in range(1,2):
        if k<=j:
            ins,outs=momentum_day_2(matrix,mass,j=j,k=k,equal=False,contrarian=False)
            port_value=portfolio_value(ins,outs,8000,k=k)
            port_value.plot()
            port_value.to_csv('Shorting/momentum_2/Turnover Rate 1'+str(j)+str(k)+'.csv')
            data['Close'].plot()
            plt.show()