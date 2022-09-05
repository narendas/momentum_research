import os
os.chdir(r'C:\Users\NarendradasT\OneDrive - Carbynetech (India ) Pvt Ltd\Desktop\Repos\momentum_research')
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import date

def var_historic(df):
    if isinstance(df, pd.DataFrame):
        return df.aggregate(var_historic)
    if isinstance(df, pd.Series):
        return -np.percentile(df,5)

def max_dd(df):
    previous_peaks=df.cummax()
    drawdown=(df-previous_peaks)/(previous_peaks)
    
    return drawdown.min()*100

ticker='^NSEI'
ticker=yf.Ticker(ticker)
nifty=ticker.history(start=date(2018,1,1),end=date(2022,1,1,))['Close']
fin=nifty.values[-1]
init=nifty.values[0]

nifty=nifty.resample('M').last()
nifty_months=len(nifty)
mean=(((fin/init)**(1/nifty_months))-1)*100
mdd=max_dd(nifty)

nifty=100*np.log(nifty/nifty.shift(1)).dropna()
d={}

std=nifty.std()

var=var_historic(nifty)

d['Portfolio']='Nifty'
d['Mean']=mean
d['Std']=std

sp=mean/std

d['Fin Wealth']=fin/init
d['Sharpe Ratio']=np.abs(sp)
d['Var 95%']=var
d['Max DD']=mdd
    
stats_df=pd.DataFrame(columns=['Portfolio','Mean','Std','Fin Wealth','Sharpe Ratio','Var 95%','Max DD'])


stats_df=pd.concat([stats_df,pd.DataFrame(d.values(),index=d.keys()).T],
                   ignore_index=True)

stats_df.to_csv('Results/nifty_2018_stats1.csv',index=False)
