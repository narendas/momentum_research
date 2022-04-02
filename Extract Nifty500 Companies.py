from tabula import read_pdf
from tabulate import tabulate
import os
import numpy as np
import pandas as pd
os.chdir(r'C:/Users/NarendradasT/OneDrive - Carbynetech (India ) Pvt Ltd/Desktop/Repos/momentum_research/Nifty 500 Companies')


final_df=pd.DataFrame()
for file in os.listdir('pdf'):
    print(file)
    df_list=read_pdf('pdf/'+file,pages="all")
    pre_df=pd.DataFrame(columns=[file.split('.')[0][-7:]])
    for df in df_list:
        for index in df.index:
            if pd.isnull(df.loc[index,df.columns[0]]):
                pass
            else:
                if df.loc[index,df.columns[0]]!='Symbol':
                    a=df.loc[index,df.columns[0]]
                    pre_df=pd.concat([pre_df,pd.DataFrame([a],columns=pre_df.columns)],ignore_index=True)
    
    pre_df=pre_df.drop_duplicates()
    pre_df=pre_df.dropna()
    final_df[file.split('.')[0][-7:]]=pre_df[file.split('.')[0][-7:]]

final_df.to_csv('Nifty 500 Companies.csv',index=False)
