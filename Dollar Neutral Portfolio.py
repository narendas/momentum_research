import os
os.chdir(r'C:\Users\NarendradasT\OneDrive - Carbynetech (India ) Pvt Ltd\Desktop\Repos\momentum_research')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

for period in ['Day','Week','Month','Year']:
    period_csv='Best '+period+'.csv'
    portfolios=pd.DataFrame()
    df=pd.read_csv(period_csv)
    df=df.loc[1:,:]
    for momentum in df['Strategy'].unique():
        mom_df=df[df['Strategy']==momentum]
        criterion=mom_df['Strategy.2'].unique()[0]
        
        strategy=mom_df['Strategy.3'].unique()[0]
        
        portfolio=[x for x in mom_df['Strategy.1'] if x in ['W-L','L-W']]
        
        if momentum=='Momentum 3':
            path=os.path.join(strategy,momentum,portfolio[0],period,criterion+'.csv')
            port_value=pd.read_csv(path,index_col=('Date'))
            port_value=port_value/port_value.loc[port_value.index[0],'Capital']
            portfolios[momentum]=port_value
        elif momentum=='Traditional Momentum':
            path=os.path.join(momentum,strategy,portfolio[0],period,criterion+'.csv')
            port_value=pd.read_csv(path,index_col=('Date'))
            port_value=port_value/port_value.loc[port_value.index[0],'Capital']
            #portfolios[momentum]=port_value
        else:
            path=os.path.join(strategy,momentum,'Turnover Rate',portfolio[0],period,criterion+'.csv')
            port_value=pd.read_csv(path,index_col=('Date'))
            port_value=port_value/port_value.loc[port_value.index[0],'Capital']
            portfolios[momentum]=port_value
    
    
    portfolios.plot()
    plt.title(period)
