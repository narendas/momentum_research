import os
os.chdir(r'C:\Users\NarendradasT\OneDrive - Carbynetech (India ) Pvt Ltd\Desktop\Repos\momentum_research')
import numpy as np
import pandas as pd
from base import momentum_matrix
from datetime import date,timedelta
from nsepy import get_history
import yfinance as yf
import matplotlib.pyplot as plt
from math import isnan

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
        
        companies=matrix.columns
        lookback=lookback1[companies]
        holding=holding1[companies]
        
        momentum=lookback.sum()
        
        positive_momentum=momentum[momentum>0]
        positive_rank=positive_momentum.rank(pct=True)
        
        #buy_companies=positive_rank[positive_rank>=0.9].index
        buy_companies=positive_rank[:10].index
        
        if len(buy_companies)>10:
            break
        if len(buy_companies)>0:
            if equal==True:
                buy_weights=pd.Series(1/len(buy_companies),index=buy_companies)
            
            else:
                buy_weights=pd.Series(index=buy_companies)
                buy_weights=positive_momentum[buy_weights.index]
                
                buy_weights=buy_weights/buy_weights.sum()
            
            buy_weights=buy_weights
            for company in buy_companies:
                ins.loc[matrix.index[i],company]=1*buy_weights[buy_weights.index==company][0]
                
        
        negative_momentum=momentum[momentum<0]
        negative_rank=negative_momentum.rank(pct=True)
        #sell_companies=negative_rank[negative_rank>=0.9].index
        sell_companies=negative_rank[-10:].index
        
        if len(sell_companies)>0:
            if equal==True:
                sell_weights=pd.Series(-1/len(sell_companies),index=sell_companies)
            else:
                sell_weights=pd.Series(index=sell_companies)
                sell_weights=negative_momentum[sell_weights.index]
                
                sell_weights=-sell_weights/sell_weights.sum()
            
            sell_weights=sell_weights
            for company in sell_companies:
                ins.loc[matrix.index[i],company]=1*sell_weights[sell_weights.index==company][0]
        
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
        
        lookback1=matrix[i+1-j:i+1]
        holding1=matrix[i+1:i+k+1]
        
        lookback_mass1=mass[i+1-j:i+1]
        holding_mass1=mass[i+1:i+k+1]
        
        companies=matrix.columns
        mass_companies=mass.columns
        common_companies=list(set(companies).intersection(mass_companies))
        
        lookback=lookback1[common_companies]
        holding=holding1[common_companies]
        lookback_mass=lookback_mass1[common_companies]
        holding_mass=holding_mass1[common_companies]
        
        lookback=lookback.dropna(axis=1)
        holding=holding.dropna(axis=1)
        lookback_mass=lookback_mass.dropna(axis=1)
        holding_mass=holding_mass.dropna(axis=1)
        
        
        if lookback.shape[1]>lookback_mass.shape[1]:
            lookback=lookback[lookback_mass.columns]
        momentum=lookback.sum()/lookback_mass.sum()
        
        positive_momentum=momentum[momentum>0]
        positive_rank=positive_momentum.rank(pct=True)
        
        #buy_companies=positive_rank[positive_rank>=0.9].index
        buy_companies=positive_rank[:10].index
        
        if len(buy_companies)>10:
            break
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
        #sell_companies=negative_rank[negative_rank>=0.9].index
        sell_companies=negative_rank[-10:].index
        
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

def portfolio_value(ins,outs,investment,k):
    cash=pd.Series(k*investment,index=pd.date_range(start=ins.index[0],end=outs.index[0]-timedelta(days=1)))
    capital_history=pd.DataFrame(index=ins.index,columns=['Capital'])
    capital_history.loc[ins.index[:k],'Capital']=investment
    date_range=pd.date_range(start=ins.index[0],end=outs.index[-1]+timedelta(days=1), freq='1D')
    holdings=pd.DataFrame(columns=ins.index,index=date_range)
    
    #holdings=holdings.resample('D').last()
    
    holdings.loc[:,:]=0
    for i in range(len(ins.index)):

        print(ins.index[i])
        market_entry=ins.loc[ins.index[i],:]
        investment=capital_history.loc[ins.index[i],'Capital']
        capital_entry=market_entry*investment
        capital_entry=capital_entry[capital_entry!=0]
        
        capital_entry=-1*capital_entry
        
        final_capital=0
        port_value=pd.DataFrame(index=holdings.index,columns=[ins.index[i]])
        for company in capital_entry.index:
            capital=capital_entry[company]
            ticker=yf.Ticker(company+'.NS')
            stock_data=ticker.history(start=ins.index[i],end=outs.index[i])
            
            
            for j in stock_data.index:
                no_of_stock=capital/stock_data.loc[j,'Open']
                
                buy_back=no_of_stock*stock_data.loc[j,'Close']
                
                port_value.loc[j,ins.index[i]]=capital+capital-buy_back
                
                capital=capital+(capital-buy_back)
            holdings.loc[:,ins.index[i]]=holdings.loc[:,ins.index[i]]+port_value.loc[:,ins.index[i]]
            returns=capital-capital_entry[company]
            final_capital+=returns
            print(company,final_capital)
        capital_history.loc[outs.index[i]+timedelta(days=1),'Capital']=investment+final_capital
    
    b=capital_history.resample('D').last()
    b.fillna(0,inplace=True)
    inv=cash.loc[cash.index[0]]
    for index in cash.index:
        inv=inv-b.loc[index,'Capital']
        cash.loc[index]=inv

    
    a=holdings.sum(axis=1)
    
    for i in range(len(a[:outs.index[-1]].index)):
        if a[a.index[i]]==0:
            a[a.index[i]]=a[a.index[i-1]]
            
    a[cash.index[0]:cash.index[-1]]=a[cash.index[0]:cash.index[-1]]+cash
    
    b=capital_history[-k:].cumsum().resample('D').last()
    b.fillna(0,inplace=True)
    
    for i in range(len(b.index)):
        if b.loc[b.index[i],'Capital']==0:
            #if b.index[i].day_name()!='Sunday' and b.index[i].day_name()!='Saturday':
                if a[b.index[i]]!=0:
                    b.loc[b.index[i],'Capital']=b.loc[b.index[i-1],'Capital']
                    
    a[b.index[0]:b.index[-1]]=a[b.index[0]:b.index[-1]]+pd.Series(b['Capital'])
    a=a[a!=0]
    return a

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

def portfolio_long_value(ins,outs,investment,k):
    cash=pd.Series(k*investment,index=pd.date_range(start=ins.index[0],end=outs.index[0]-timedelta(days=1)))
    capital_history=pd.DataFrame(index=ins.index,columns=['Capital'])
    capital_history.loc[ins.index[:k],'Capital']=investment
    date_range=pd.date_range(start=ins.index[0],end=outs.index[-1]+timedelta(days=1), freq='1D')
    holdings=pd.DataFrame(columns=ins.index,index=date_range)
    
    #holdings=holdings.resample('D').last()
    
    holdings.loc[:,:]=0
    for i in range(len(ins.index)):
        print(ins.index[i])
        market_entry=ins.loc[ins.index[i],:]
        investment=capital_history.loc[ins.index[i],'Capital']
        capital_entry=market_entry*investment
        capital_entry=capital_entry[capital_entry!=0]
        
        final_capital=0
        print(len(capital_entry))
        for company in capital_entry.index:
            port_value=pd.DataFrame(index=holdings.index,columns=[ins.index[i]])
            capital=capital_entry[company]
            
            ticker=yf.Ticker(company+'.NS')
            stock_data=ticker.history(start=ins.index[i],end=outs.index[i])
            
            if len(stock_data)>0:
                no_of_stock=capital/stock_data.loc[stock_data.index[0],'Open']
                for j in stock_data.index:
                    if isnan(stock_data.loc[j,'Close']):
                        break
                    else:
                        daily_value=no_of_stock*stock_data.loc[j,'Close']
                        port_value.loc[j,ins.index[i]]=daily_value
                
                if isnan(port_value.loc[ins.index[i],ins.index[i]]):
                    port_value.loc[ins.index[i],ins.index[i]]=capital
                port_value.loc[ins.index[i]:outs.index[i],ins.index[i]].fillna(method='ffill',inplace=True)
                holdings.loc[:,ins.index[i]]=holdings.loc[:,ins.index[i]]+port_value.loc[:,ins.index[i]]
                returns=daily_value-capital_entry[company]
                final_capital+=returns
            
            if len(stock_data)==0:
                print(company)
                holdings.loc[ins.index[i]:outs.index[i],ins.index[i]]=holdings.loc[ins.index[i]:outs.index[i],ins.index[i]]+capital
                final_capital+=0
        capital_history.loc[outs.index[i]+timedelta(days=1),'Capital']=investment+final_capital
    
    b=capital_history.resample('D').last()
    b.fillna(0,inplace=True)
    inv=cash.loc[cash.index[0]]
    for index in cash.index:
        inv=inv-b.loc[index,'Capital']
        cash.loc[index]=inv

    cash=cash[cash!=0]
    a=holdings.sum(axis=1)
    if len(cash)>0:
        for i in range(len(a[:cash.index[-1]].index)):
            if a[a.index[i]]==0:
                a[a.index[i]]=a[a.index[i-1]]
                
        a[cash.index[0]:cash.index[-1]]=a[cash.index[0]:cash.index[-1]]+cash
    
    b=capital_history[-k:].cumsum().resample('D').last()
    b.fillna(0,inplace=True)
    
    for i in range(len(a[:outs.index[-1]])):
        if a[a.index[i]]==0:
            a[a.index[i]]=a[a.index[i-1]]
            
    for i in range(len(b.index)):
        if b.loc[b.index[i],'Capital']==0:
            if a[b.index[i]]!=0:
                b.loc[b.index[i],'Capital']=b.loc[b.index[i-1],'Capital']
                    
    a[b.index[0]:b.index[-1]]=a[b.index[0]:b.index[-1]]+pd.Series(b['Capital'])
    a=a[a!=0]
    return a

ticker='^NSEI'
ticker=yf.Ticker(ticker)
data=ticker.history(start=date(2015,1,1),end=date(2021,11,30))
matrix=pd.read_csv('Momentum Matrix/Year/Inverse Turnover Rate 1/matrix.csv')
matrix.index=pd.to_datetime(matrix['Date'])
matrix.drop('Date',axis=1,inplace=True)
for j in range(1,8):
    for k in range(1,8):
        if k<=j:
            if os.path.exists('Buying/Month/momentum_1/Inverse Turnover Rate 1/'+str(j)+str(k)+'.csv'):
                print('Already Exists')
            else:
                ins,outs=momentum_1(matrix,j=j,k=k,equal=False,contrarian=True)
                port_value=portfolio_long_value(ins,outs,8000,k=k)
                port_value.to_csv('Buying/Year/Contrarian momentum_1/Inverse Turnover Rate 1/'+str(j)+str(k)+'.csv')
                port_value.plot()
                a=k*data['Close']
                a.plot()
                plt.show()


ticker='^NSEI'
ticker=yf.Ticker(ticker)
data=ticker.history(start=date(2015,1,1),end=date(2021,11,30))
matrix=pd.read_csv('Momentum Matrix/Week/Turnover Rate 1/matrix.csv')
matrix.index=pd.to_datetime(matrix['Date'])
matrix.drop('Date',axis=1,inplace=True)


mass=pd.read_csv('Momentum Mass/Week/Turnover Rate 1/matrix.csv')
mass.index=pd.to_datetime(mass['Date'])
mass.drop('Date',axis=1,inplace=True)
for j in range(1,8):
    for k in range(1,8):
        if k<=j:
            if os.path.exists('Buying/Month/momentum_1/Inverse Turnover Rate 1/'+str(j)+str(k)+'.csv'):
                print('Already Exists')
            else:
                ins,outs=momentum_2(matrix,mass,j=j,k=k,equal=True,contrarian=True)
                port_value=portfolio_long_value(ins,outs,8000,k=k)
                port_value.to_csv('Buying/Week/momentum_2/Turnover Rate 1/'+str(j)+str(k)+'.csv')
                port_value.plot()
                a=k*data['Close']
                a.plot()
                plt.show()