import os
os.chdir(r'C:/Users/HP/Desktop/Repos/momentum_research')
import numpy as np
import pandas as pd
from base import get_resampled_nse_data,get_all_stocks,get_resampled_data
from datetime import date,timedelta
from nsepy import get_history
import yfinance as yf
def momentum_matrix(mass,velocity,resample):
    stocks=get_all_stocks()
    momentum_matrix=pd.DataFrame()
    for stock in stocks:
        print(stock)
        try:
            resampled_data=get_resampled_data(stock,start=date(2015,1,1),end=date(2015,11,30),period=resample)
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
            resampled_data=get_resampled_data(stock,start=date(2015,1,1),end=date(2015,11,30),period=resample)
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
        sell_companies=negative_rank[negative_rank<=0.1].index
        
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
        
        if len(sell_companies)>0 and len(buy_companies)>0:
            ins.loc[matrix.index[i],:]=ins.loc[matrix.index[i],:]*0.5
    
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
            
            buy_weights=buy_weights
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
            
            sell_weights=sell_weights
            for company in sell_companies:
                ins.loc[matrix.index[i],company]=sell_weights[sell_weights.index==company][0]
        
        if len(sell_companies)>0 and len(buy_companies)>0:
            ins.loc[matrix.index[i],:]=ins.loc[matrix.index[i],:]*0.5
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
            
            buy_weights=buy_weights
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
            
            sell_weights=sell_weights
            for company in sell_companies:
                ins.loc[matrix.index[i],company]=sell_weights[sell_weights.index==company][0]
        
        if len(sell_companies)>0 and len(buy_companies)>0:
            ins.loc[matrix.index[i],:]=ins.loc[matrix.index[i],:]*0.5
    
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
            ticker=yf.Ticker(index+'.NS')
            stock_data=ticker.history(start=ins.index[i],end=outs.index[i])
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
                capital=capital+(capital-bought_back)
            capital_returns[index]=returns
            
        #short_returns=capital_returns.sum()
        historical_returns.loc[outs.index[i],capital_returns.index]=capital_returns
        
        
    return historical_returns


matrix=momentum_matrix('Turnover Rate 1','Log Returns','W')
momentumres_1=pd.DataFrame(columns=['1','2','3','4','5','6','7','8'],index=['1','2','3','4','5','6','7','8'])
for j in range(1,9):
    for k in range(1,9):
        if k<=j:
            ins,outs=momentum_1(matrix,j=j,k=k,equal=False,contrarian=False)
            returns=sell_strategy(100000,ins,outs)
            a_1=returns.sum(axis=1)
            
            print('Momentum 1:',a_1.sum())
            
            momentumres_1.loc[str(k),str(j)]=a_1.sum()



matrix_mass=mass('Turnover Rate 1','W')
momentumres_2=pd.DataFrame(columns=['1','2','3','4','5','6','7','8'],index=['1','2','3','4','5','6','7','8'])
for j in range(1,9):
    for k in range(1,9):
        if k<=j:
            ins,outs=momentum_2(matrix,matrix_mass,j=j,k=k,equal=False,contrarian=False)
            returns=sell_strategy(100000,ins,outs)
            a_2=returns.sum(axis=1)
            
            print('Momentum 2:',a_2.sum())
            
            momentumres_2.loc[str(k),str(j)]=a_2.sum()

matrix_sd=mass('Log Returns','W')
momentumres_3=pd.DataFrame(columns=['1','2','3','4','5','6','7','8'],index=['1','2','3','4','5','6','7','8'])
for j in range(1,9):
    for k in range(1,9):
        if k<=j:
            ins,outs=momentum_3(matrix_sd,j=j,k=k,equal=False,contrarian=False)
            returns=sell_strategy(100000,ins,outs)
            a_3=returns.sum(axis=1)
            
            print('Momentum 3:',a_3.sum())
            
            momentumres_3.loc[str(k),str(j)]=a_3.sum()