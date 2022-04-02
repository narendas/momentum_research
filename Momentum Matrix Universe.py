import os
os.chdir(r'C:\Users\NarendradasT\OneDrive - Carbynetech (India ) Pvt Ltd\Desktop\Repos\momentum_research')
from nsetools import Nse
import pandas as pd
from base import get_resampled_data
from datetime import date
nse=Nse()
import string

def get_all_stocks():
    all_stock_codes=nse.get_stock_codes()
    stock_list=[]
    for key, value in all_stock_codes.items():
        stock_list.append(key)
    return stock_list[1:]

def momentum_matrix(mass,velocity,resample,start,end):
    if os.path.exists('Momentum Matrix/Day/'+mass+'/matrix.csv'):
        for letter in string.ascii_uppercase:
            if letter>='K':
                stocks=get_all_stocks()
                stocks=[a for a in stocks if a.startswith(letter)]
                momentum_matrix=pd.read_csv('Momentum Matrix/Day/'+mass+'/matrix.csv')
                
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
                momentum_matrix.to_csv('Momentum Matrix/Day/'+mass+'/matrix.csv')
    
    else:
        stocks=get_all_stocks()
        stocks=stocks[:7]
        momentum_matrix=pd.DataFrame()
        for stock in stocks:
            print(stock)
            try:
                resampled_data=get_resampled_data(stock,start=start,end=end,period=resample)
                momentum=resampled_data[mass]*resampled_data[velocity]  
                momentum_matrix[stock]=momentum
            except:
                pass
        momentum_matrix.to_csv('Momentum Matrix/Day/'+mass+'/matrix.csv')
    return momentum_matrix

def momentum_mass(mass,resample,start,end):
    if os.path.exists('Momentum Mass/Year/'+mass+'/matrix.csv'):
        for letter in string.ascii_uppercase:
            if letter>='A':
                stocks=get_all_stocks()
                stocks=[a for a in stocks if a.startswith(letter)]
                momentum_matrix=pd.read_csv('Momentum Mass/Year/'+mass+'/matrix.csv')
                
                momentum_matrix.index=pd.to_datetime(momentum_matrix['Date'])
                
                momentum_matrix.drop('Date',axis=1,inplace=True)
                
                for stock in stocks:
                    print(stock)
                    try:
                        resampled_data=get_resampled_data(stock,start=start,end=end,period=resample)
                        momentum_matrix[stock]=resampled_data[mass]
                    except:
                        pass
                #momentum_matrix.to_csv('Momentum Mass/Year/'+mass+'/matrix.csv')
    
    else:
        stocks=get_all_stocks()
        stocks=stocks[:7]
        momentum_matrix=pd.DataFrame()
        for stock in stocks:
            print(stock)
            try:
                resampled_data=get_resampled_data(stock,start=start,end=end,period=resample)
                momentum_matrix[stock]=resampled_data[mass]
            except:
                pass
        momentum_matrix.to_csv('Momentum Mass/Year/'+mass+'/matrix.csv')
    return momentum_matrix

#matrix=momentum_matrix('Inverse Turnover Rate 1','Log Returns','D',start=date(2015,1,1),end=date(2021,11,30))
matrix=momentum_mass('Turnover Rate 1','Y',start=date(2015,1,1),end=date(2021,11,30))