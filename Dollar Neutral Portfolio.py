import os
os.chdir(r'C:\Users\NarendradasT\OneDrive - Carbynetech (India ) Pvt Ltd\Desktop\Repos\momentum_research')
import pandas as pd
import numpy as np



path='Contrarian Strategy/Momentum 1/Turnover Rate/L-W'
for period in os.listdir(path):
    for file in os.listdir(os.path.join(path,period)):
        data=pd.read_csv(os.path.join(path,period,file),index_col=('Date'))
        data.index=pd.to_datetime(data.index)
        
        data=data/100000
        data.plot()
        break
    break