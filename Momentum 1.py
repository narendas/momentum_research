import pandas as pd
from base import momentum_matrix
from datetime import date,timedelta
from nsepy import get_history
import yfinance as yf
import matplotlib.pyplot as plt
from math import isnan
import numpy as np
import os
os.chdir(r'C:\Users\NarendradasT\OneDrive - Carbynetech (India ) Pvt Ltd\Desktop\Repos\momentum_research')

def momentum_1(matrix,j,k,equal=True,contrarian=False):    
    prev_comb=''
    ins=pd.DataFrame(columns=matrix.columns,index=matrix.index[j-1:-k])
    outs=pd.DataFrame(columns=matrix.columns,index=matrix.index[j-1+k:])
    for i in range(j-1,len(matrix.index)-k):
        year=str(matrix.index[i].year)
        month=str(matrix.index[i].month_name())[:3]
        
        comb=month+year
        
        lookback1=matrix[i+1-j:i+1]
        holding1=matrix[i+1:i+k+1]
        
        nifty500companies=pd.read_csv('Nifty 500 Companies/Nifty 500 Companies.csv')
        companies=list(nifty500companies.loc[:,comb])
        companies=[company for company in companies if company in matrix.columns]
        lookback=lookback1[companies]
        holding=holding1[companies]
        
        momentum=lookback.sum()
        
        positive_momentum=momentum[momentum>0]
        positive_momentum=positive_momentum.sort_values(ascending=False)
        #positive_rank=positive_momentum.rank(pct=True)
        
        #buy_companies=positive_rank[positive_rank>=0.9].index
        buy_companies=positive_momentum[:10].index
        
        if len(buy_companies)>0:
            if equal==True:
                buy_weights=pd.Series(1/len(buy_companies),index=buy_companies)
            
            else:
                buy_weights=pd.Series(index=buy_companies)
                buy_weights=positive_momentum[buy_weights.index]
                
                buy_weights=buy_weights/buy_weights.sum()
            
            #buy_weights=buy_weights
            for company in buy_companies:
                ins.loc[matrix.index[i],company]=1*buy_weights[buy_weights.index==company][0]
                
        
        negative_momentum=momentum[momentum<0]
        negative_momentum=negative_momentum.sort_values()
        #negative_rank=negative_momentum.rank(pct=True)
        #sell_companies=negative_rank[negative_rank>=0.9].index
        sell_companies=negative_momentum[:10].index
        
        if len(sell_companies)>0:
            if equal==True:
                sell_weights=pd.Series(-1/len(sell_companies),index=sell_companies)
            else:
                sell_weights=pd.Series(index=sell_companies)
                sell_weights=negative_momentum[sell_weights.index]
                
                sell_weights=-sell_weights/sell_weights.sum()
            
            #sell_weights=sell_weights
            for company in sell_companies:
                ins.loc[matrix.index[i],company]=1*sell_weights[sell_weights.index==company][0]
        
        if len(sell_companies)>0 and len(buy_companies)>0:
            ins.loc[matrix.index[i],:]=ins.loc[matrix.index[i],:]*0.5
        else:
            ins.loc[matrix.index[i],:]=ins.loc[matrix.index[i],:]*0
    
    outs=pd.DataFrame(-np.array(ins),index=outs.index,columns=outs.columns)
    
    ins.fillna(0,inplace=True)
    outs.fillna(0,inplace=True)
    
    ins.index=ins.index+timedelta(days=1)
    
    if contrarian==True:
        ins=-ins
        outs=-outs
    return ins,outs

if __name__=='__main__':
    matrix=pd.read_csv('Momentum/Momentum Matrix/Week/Turnover Rate/matrix.csv')
    matrix['Date']=pd.to_datetime(matrix['Date'])
    matrix.index=matrix['Date']
    matrix.drop('Date',axis=1,inplace=True)
    
    j=1
    k=1
    ins,outs=momentum_1(matrix,j,k,equal=True,contrarian=False)