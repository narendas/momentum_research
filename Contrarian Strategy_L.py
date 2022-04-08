import os
os.chdir(r'C:\Users\NarendradasT\OneDrive - Carbynetech (India ) Pvt Ltd\Desktop\Repos\momentum_research')
import pandas as pd
from datetime import timedelta
from math import isnan
import yfinance as yf
from Momentum_1 import momentum_1
from Momentum_2 import momentum_2
from Momentum_3 import momentum_3
import matplotlib.pyplot as plt

def strategy_l(ins,outs,investment,k):
    cash=pd.Series(k*investment,index=pd.date_range(start=ins.index[0],end=outs.index[0]))
    capital_history=pd.DataFrame(index=ins.index,columns=['Capital'])
    capital_history.loc[ins.index[:k],'Capital']=investment
    date_range=pd.date_range(start=ins.index[0],end=outs.index[-1], freq='1D')
    holdings=pd.DataFrame(columns=ins.index,index=date_range)
    holdings.loc[:,:]=0
    for i in range(len(ins.index)):
        print(ins.index[i])
        market_entry=ins.loc[ins.index[i],:]
        market_entry=market_entry*2
        investment=capital_history.loc[ins.index[i],'Capital']
        capital_entry=market_entry*investment
        
        capital_entry=capital_entry[capital_entry>0]
        final_capital=0
        print(len(capital_entry))
        for company in capital_entry.index:
            port_value=pd.DataFrame(index=holdings.index,columns=[ins.index[i]])
            capital=capital_entry[company]
            
            stock_data=pd.read_csv('Historical Price Data/'+company+'.csv')
            stock_data['Date']=pd.to_datetime(stock_data['Date'])
            stock_data.index=stock_data['Date']
            stock_data.drop('Date',axis=1,inplace=True)
            
            stock_data=stock_data.loc[ins.index[i]:outs.index[i],:]
        
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
    
    #below for code is to get cash when the positions are closed for final time
    for i in range(-k,-1):
        holdings.loc[outs.index[i]:,ins.index[i]].fillna(method='ffill',inplace=True)
        
    portfolio_value=holdings.sum(axis=1)
    daily_capital_history=capital_history.resample('D').last()
    daily_capital_history.fillna(0,inplace=True)
    
    #cash reserves during the starting of investment cycle till all the holding periods have started
    inv=cash.loc[cash.index[0]]
    for index in cash.index:
        inv=inv-daily_capital_history.loc[index,'Capital']
        cash.loc[index]=inv
    
    
    for index in cash.index:
        portfolio_value.loc[index]=portfolio_value.loc[index]+cash[index]
    
    portfolio_value=pd.DataFrame(portfolio_value,columns=['Capital'])
    portfolio_value.index.rename('Date',inplace=True)
    return portfolio_value

if __name__=='__main__':
    ticker='^NSEI'
    ticker=yf.Ticker(ticker)
    
    investment=50000
    period='Week'
    mass='Turnover Rate'
    
    if period=='Day':    
        max_iter=8
    elif period=='Week':    
        max_iter=9
    elif period=='Month':    
        max_iter=13
    elif period=='Year':    
        max_iter=4
    '''MOMENTUM 1'''
    for j in range(1,max_iter):
        for k in range(1,max_iter):
            print(j,k)
            if os.path.exists('Contrarian Strategy/Momentum 1/'+mass+'/L/'+period+'/'+str(j)+'-'+str(k)+'.csv'):
                print('Already Exists')
                portfolio_value=pd.read_csv('Contrarian Strategy/Momentum 1/'+mass+'/L/'+period+'/'+str(j)+'-'+str(k)+'.csv')
                portfolio_value['Date']=pd.to_datetime(portfolio_value['Date'])
                portfolio_value.index=portfolio_value['Date']
                portfolio_value.drop('Date',axis=1,inplace=True)
                
                nifty=ticker.history(start=portfolio_value.index[0],end=portfolio_value.index[-1])
                nifty=(nifty['Close']-nifty.loc[nifty.index[0],'Close'])/nifty.loc[nifty.index[0],'Close']
                
                portfolio_value=(portfolio_value-k*investment)/(k*investment)
                portfolio_value.plot()
                nifty.plot()
                plt.show()
            else:
                matrix=pd.read_csv('Momentum/Momentum Matrix/'+period+'/'+mass+'/matrix.csv')
                matrix['Date']=pd.to_datetime(matrix['Date'])
                matrix.index=matrix['Date']
                matrix.drop('Date',axis=1,inplace=True)
                
                ins,outs=momentum_1(matrix,j,k,equal=True,contrarian=True)
                
                try:
                    portfolio_value=strategy_l(ins,outs,investment,k)
                except:
                    break
                portfolio_value.to_csv('Contrarian Strategy/Momentum 1/'+mass+'/L/'+period+'/'+str(j)+'-'+str(k)+'.csv')
                
                nifty=ticker.history(start=portfolio_value.index[0],end=portfolio_value.index[-1])
                nifty=(nifty['Close']-nifty.loc[nifty.index[0],'Close'])/nifty.loc[nifty.index[0],'Close']
                
                portfolio_value=(portfolio_value-k*investment)/(k*investment)
                portfolio_value.plot()
                nifty.plot()
                plt.show()

    '''MOMENTUM 2'''
    for j in range(1,max_iter):
        for k in range(1,max_iter):
            print(j,k)
            if os.path.exists('Contrarian Strategy/Momentum 2/'+mass+'/L/'+period+'/'+str(j)+'-'+str(k)+'.csv'):
                print('Already Exists')
                portfolio_value=pd.read_csv('Contrarian Strategy/Momentum 2/'+mass+'/L/'+period+'/'+str(j)+'-'+str(k)+'.csv')
                portfolio_value['Date']=pd.to_datetime(portfolio_value['Date'])
                portfolio_value.index=portfolio_value['Date']
                portfolio_value.drop('Date',axis=1,inplace=True)
                
                nifty=ticker.history(start=portfolio_value.index[0],end=portfolio_value.index[-1])
                nifty=(nifty['Close']-nifty.loc[nifty.index[0],'Close'])/nifty.loc[nifty.index[0],'Close']
                
                portfolio_value=(portfolio_value-k*investment)/(k*investment)
                portfolio_value.plot()
                nifty.plot()
                plt.show()
            else:
                matrix=pd.read_csv('Momentum/Momentum Matrix/'+period+'/'+mass+'/matrix.csv')
                matrix['Date']=pd.to_datetime(matrix['Date'])
                matrix.index=matrix['Date']
                matrix.drop('Date',axis=1,inplace=True)
                
                matrix_mass=pd.read_csv('Momentum/Momentum Mass/'+period+'/'+mass+'/matrix.csv')
                matrix_mass.index=pd.to_datetime(matrix_mass['Date'])
                matrix_mass.drop('Date',axis=1,inplace=True)
                
                ins,outs=momentum_2(matrix,matrix_mass,j,k,equal=True,contrarian=True)
                
                try:
                    portfolio_value=strategy_l(ins,outs,investment,k)
                except:
                    break
                portfolio_value.to_csv('Contrarian Strategy/Momentum 2/'+mass+'/L/'+period+'/'+str(j)+'-'+str(k)+'.csv')
                
                nifty=ticker.history(start=portfolio_value.index[0],end=portfolio_value.index[-1])
                nifty=(nifty['Close']-nifty.loc[nifty.index[0],'Close'])/nifty.loc[nifty.index[0],'Close']
                
                portfolio_value=(portfolio_value-k*investment)/(k*investment)
                portfolio_value.plot()
                nifty.plot()
                plt.show()
                
    '''MOMENTUM 3'''
    for j in range(1,max_iter):
        for k in range(1,max_iter):
            print(j,k)
            if os.path.exists('Contrarian Strategy/Momentum 3/L/'+period+'/'+str(j)+'-'+str(k)+'.csv'):
                print('Already Exists')
                portfolio_value=pd.read_csv('Contrarian Strategy/Momentum 3/L/'+period+'/'+str(j)+'-'+str(k)+'.csv')
                portfolio_value['Date']=pd.to_datetime(portfolio_value['Date'])
                portfolio_value.index=portfolio_value['Date']
                portfolio_value.drop('Date',axis=1,inplace=True)
                
                nifty=ticker.history(start=portfolio_value.index[0],end=portfolio_value.index[-1])
                nifty=(nifty['Close']-nifty.loc[nifty.index[0],'Close'])/nifty.loc[nifty.index[0],'Close']
            
                portfolio_value=(portfolio_value-k*investment)/(k*investment)
                portfolio_value.plot()
                nifty.plot()
                plt.show()
            else:
                matrix=pd.read_csv('Momentum/Momentum Matrix 3/'+period+'/matrix.csv')
                matrix['Date']=pd.to_datetime(matrix['Date'])
                matrix.index=matrix['Date']
                matrix.drop('Date',axis=1,inplace=True)
                
                ins,outs=momentum_3(matrix,j,k,equal=True,contrarian=True)
                try:
                    portfolio_value=strategy_l(ins,outs,investment,k)
                except:
                    break
                portfolio_value.to_csv('Contrarian Strategy/Momentum 3/L/'+period+'/'+str(j)+'-'+str(k)+'.csv')
                
                nifty=ticker.history(start=portfolio_value.index[0],end=portfolio_value.index[-1])
                nifty=(nifty['Close']-nifty.loc[nifty.index[0],'Close'])/nifty.loc[nifty.index[0],'Close']
                
                portfolio_value=(portfolio_value-k*investment)/(k*investment)
                portfolio_value.plot()
                nifty.plot()
                plt.show()