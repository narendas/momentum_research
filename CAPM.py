import os
os.chdir(r'C:\Users\NarendradasT\OneDrive - Carbynetech (India ) Pvt Ltd\Desktop\Repos\momentum_research')
import statsmodels.api as sm
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import date


period='Day'

rf=pd.read_csv('Risk Free.csv',index_col='Date')['Rate']
rf.index=pd.to_datetime(rf.index)
rf=rf.resample('M').last()
rf=rf.apply(lambda x: (np.power(x,1/12)-1))

ticker=yf.Ticker('^NSEI')
nifty=ticker.history(start=date(2014,1,1), end=date(2022,1,1))['Close']
nifty=nifty.resample('M').last()
nifty=100*np.log(nifty/nifty.shift(1)).dropna()


risks_df=pd.read_csv(os.path.join('Results',period,'risks.csv'))
for momentum in risks_df['Momentum'].unique():
    mom_df=risks_df[risks_df['Momentum']==momentum].reset_index(drop=True)
    for mass in mom_df['Mass'].unique():
        mass_df=mom_df[mom_df['Mass']==mass].reset_index(drop=True)
        for strat in mass_df['Strategy'].unique():
            best_df=mass_df[mass_df['Strategy']==strat].reset_index(drop=True)
            crit=best_df['Criterion'].item()
            port=best_df['Portfolio'].item()
            
            print('==================='+momentum+' '+mass+' '+strat+' '+crit+' '+port+'============================')
            if momentum=='Momentum 3':
                best_df=pd.read_csv(os.path.join(strat,momentum,port,period,crit+'.csv'),index_col='Date')
            else:
                best_df=pd.read_csv(os.path.join(strat,momentum,mass,port,period,crit+'.csv'),index_col='Date')

            best_df.index=pd.to_datetime(best_df.index)
            best_df=best_df.resample('M').last()
            best_df['Return']=100*np.log(best_df['Capital']/best_df['Capital'].shift(1)).dropna()

            capm_df=pd.DataFrame()
            capm_df['Port Return']=best_df['Return']
            capm_df['RF Return']=rf
            capm_df['Market Return']=nifty
            capm_df['Excess Returns']=capm_df['Port Return']-capm_df['RF Return']
            capm_df['Market Excess Returns']=capm_df['Market Return']-capm_df['RF Return']
            
            x=capm_df['Market Excess Returns'].dropna()
            y=capm_df['Excess Returns'].dropna()
            
            x=sm.add_constant(x)
            
            model=sm.OLS(y,x)
            results=model.fit()
            
            print(results.summary2())