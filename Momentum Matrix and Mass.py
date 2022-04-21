import os
os.chdir(r'C:\Users\NarendradasT\OneDrive - Carbynetech (India ) Pvt Ltd\Desktop\Repos\momentum_research')
from nsetools import Nse
import pandas as pd
from base import get_resampled_data
from datetime import date
nse=Nse()
import string

def get_all_stocks():
    nifty500=pd.read_csv('Nifty 500 Companies/Nifty 500 Companies.csv')
    
    #GET LIST OF COMPANIES THAT WERE PART OF NIFTY500
    all_companies=[]
    for column in nifty500.columns:
        companies=list(nifty500.loc[:,column])
        
        for company in companies:
            if company not in all_companies:
                all_companies.append(company)
    return all_companies

def momentum_matrix(mass,velocity,resample,start,end,period):
    if os.path.exists('Momentum/Momentum Matrix/'+period+'/'+mass+'/matrix.csv'):
        for letter in string.ascii_uppercase:
            if letter>='A':
                stocks=get_all_stocks()
                stocks=[a for a in stocks if a.startswith(letter)]
                momentum_matrix=pd.read_csv('Momentum/Momentum Matrix/'+period+'/'+mass+'/matrix.csv')
                
                momentum_matrix.index=pd.to_datetime(momentum_matrix['Date'])
                
                momentum_matrix.drop('Date',axis=1,inplace=True)
                
                for stock in stocks:
                    print(stock)
                    try:
                        resampled_data=get_resampled_data(stock,start=start,end=end,period=resample)
                        momentum=resampled_data[mass]*resampled_data[velocity]  
                        momentum_matrix[stock]=momentum
                    except:
                        pass
                momentum_matrix.to_csv('Momentum/Momentum Matrix/'+period+'/'+mass+'/matrix.csv')
    
    else:
        stocks=get_all_stocks()
        stocks=stocks[:1]
        momentum_matrix=pd.DataFrame()
        for stock in stocks:
            print(stock)
            try:
                resampled_data=get_resampled_data(stock,start=start,end=end,period=resample)
                momentum=resampled_data[mass]*resampled_data[velocity]  
                momentum_matrix[stock]=momentum
            except:
                pass
        momentum_matrix.to_csv('Momentum/Momentum Matrix/'+period+'/'+mass+'/matrix.csv')
    return momentum_matrix

def momentum_mass(mass,resample,start,end,period):
    if os.path.exists('Momentum/Momentum Mass/'+period+'/'+mass+'/matrix.csv'):
        for letter in string.ascii_uppercase:
            if letter>='A':
                stocks=get_all_stocks()
                stocks=[a for a in stocks if a.startswith(letter)]
                momentum_matrix=pd.read_csv('Momentum/Momentum Mass/'+period+'/'+mass+'/matrix.csv')
                
                momentum_matrix.index=pd.to_datetime(momentum_matrix['Date'])
                
                momentum_matrix.drop('Date',axis=1,inplace=True)
                
                for stock in stocks:
                    print(stock)
                    try:
                        resampled_data=get_resampled_data(stock,start=start,end=end,period=resample)
                        momentum_matrix[stock]=resampled_data[mass]
                    except:
                        pass
                momentum_matrix.to_csv('Momentum/Momentum Mass/'+period+'/'+mass+'/matrix.csv')
    
    else:
        stocks=get_all_stocks()
        stocks=stocks[:1]
        momentum_matrix=pd.DataFrame()
        for stock in stocks:
            print(stock)
            try:
                resampled_data=get_resampled_data(stock,start=start,end=end,period=resample)
                momentum_matrix[stock]=resampled_data[mass]
            except:
                pass
        momentum_matrix.to_csv('Momentum/Momentum Mass/'+period+'/'+mass+'/matrix.csv')
    return momentum_matrix


def momentum_matrix3(velocity,resample,start,end,period):
    if os.path.exists('Momentum/Momentum Matrix 3/'+period+'/matrix.csv'):
        for letter in string.ascii_uppercase:
            if letter>='A':
                stocks=get_all_stocks()
                stocks=[a for a in stocks if a.startswith(letter)]
                momentum_matrix=pd.read_csv('Momentum/Momentum Matrix 3/'+period+'/matrix.csv')
                
                momentum_matrix.index=pd.to_datetime(momentum_matrix['Date'])
                
                momentum_matrix.drop('Date',axis=1,inplace=True)
                
                for stock in stocks:
                    print(stock)
                    try:
                        resampled_data=get_resampled_data(stock,start=start,end=end,period=resample)
                        momentum=resampled_data[velocity]  
                        momentum_matrix[stock]=momentum
                    except:
                        pass
                momentum_matrix.to_csv('Momentum/Momentum Matrix 3/'+period+'/matrix.csv')
    
    else:
        stocks=get_all_stocks()
        stocks=stocks[:1]
        momentum_matrix=pd.DataFrame()
        for stock in stocks:
            print(stock)
            try:
                resampled_data=get_resampled_data(stock,start=start,end=end,period=resample)
                momentum=resampled_data[velocity]  
                momentum_matrix[stock]=momentum
            except:
                pass
        momentum_matrix.to_csv('Momentum/Momentum Matrix 3/'+period+'/matrix.csv')
    return momentum_matrix

mass='Turnover Rate'
velocity='Log Returns'
start=date(2014,1,1)
end=date(2022,1,1)
for period in ['Day','Week','Month','Year']:
    resample=period[0]
    matrix=momentum_matrix(mass,velocity,resample,start,end,period)

mass='Inverse Turnover Rate'
velocity='Log Returns'
start=date(2014,1,1)
end=date(2022,1,1)
for period in ['Day','Week','Month','Year']:
    resample=period[0]
    matrix=momentum_matrix(mass,velocity,resample,start,end,period)

mass='Turnover Rate'
velocity='Log Returns'
start=date(2014,1,1)
end=date(2022,1,1)
for period in ['Day','Week','Month','Year']:
    resample=period[0]
    matrix=momentum_mass(mass,resample,start,end,period)

mass='Inverse Turnover Rate'
velocity='Log Returns'
start=date(2014,1,1)
end=date(2022,1,1)
for period in ['Day','Week','Month','Year']:
    resample=period[0]
    matrix=momentum_mass(mass,resample,start,end,period)

velocity='Log Returns'
start=date(2014,1,1)
end=date(2022,1,1)
for period in ['Day','Week','Month','Year']:
    resample=period[0]
    matrix=momentum_matrix3(velocity,resample,start,end,period)

mass='Unity'
velocity='Log Returns'
start=date(2014,1,1)
end=date(2022,1,1)
for period in ['Day','Week','Month','Year']:
    resample=period[0]
    matrix=momentum_matrix(mass,velocity,resample,start,end,period)
