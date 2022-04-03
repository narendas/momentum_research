import os
os.chdir(r'C:/Users/NarendradasT/OneDrive - Carbynetech (India ) Pvt Ltd/Desktop/Repos/momentum_research/')
import pandas as pd
from datetime import date
import yfinance as yf
import string


nifty500=pd.read_csv('Nifty 500 Companies/Nifty 500 Companies.csv')

#GET LIST OF COMPANIES THAT WERE PART OF NIFTY500
all_companies=[]
for column in nifty500.columns:
    companies=list(nifty500.loc[:,column])
    
    for company in companies:
        if company not in all_companies:
            all_companies.append(company)

#GET HISTORICAL PRICE DATA OF ALL COMPANIES THAT WERE PART OF NIFTY500
for company in all_companies:
    print(company)
    if os.path.exists('Historical Price Data/'+company+'.csv'):
        pass
    else:
        try:
            ticker=yf.Ticker(company+'.NS')
            data=ticker.history(start=date(2014,1,1),end=date(2022,1,1))
            data.to_csv('Historical Price Data/'+company+'.csv')
        except:
            print(company,' not found')

#REMOVE EMPTY CSV FILES FROM HISTORICAL PRICE DATA FOLDER
for file in os.listdir('Historical Price Data'):
    data=pd.read_csv('Historical Price Data/'+file)
    if len(data)==0:
        os.remove('Historical Price Data/'+file)


#ADD HISTORICAL OUTSTANDING SHARES DATA
failed_companies=[]

for file in os.listdir('Historical Price Data'):
    for letter in string.ascii_uppercase:
        if letter>='A':
            if file.startswith(letter):
                print(file)
                data=pd.read_csv('Historical Price Data/'+file)
                data['Date']=pd.to_datetime(data['Date'])
                data.index=data['Date']
                data.drop('Date',axis=1,inplace=True)
                
                data['Outstanding Shares']=0
                
                stock=file.split('.')[0]
                ticker=yf.Ticker(stock+'.NS')
                try:
                    data.loc[data.index[len(data)-1],'Outstanding Shares']=ticker.get_info()['sharesOutstanding']
                except:
                    failed_companies.append(file)
                    break
                prev_index=data.index[len(data)-1]
                for index in data[:-1].index[::-1]:
                    if data.loc[prev_index,'Stock Splits']!=0:
                        data.loc[index,'Outstanding Shares']=data.loc[prev_index,'Outstanding Shares']/data.loc[prev_index,'Stock Splits']
                    else:
                        data.loc[index,'Outstanding Shares']=data.loc[prev_index,'Outstanding Shares']
                    prev_index=index
                
                data.to_csv('Historical Price Data/'+file)


#GET OUTSTANDING SHARES OF COMPANIES THE CODE FAILED TO CAPTURE IN ABOVE CODE
failed_companies=pd.read_csv('Failed Companies/Failed Companies.csv')

for index in failed_companies.index:
    company=failed_companies.loc[index,'Company']
    oshares=int(failed_companies.loc[index,'Outstanding Shares'])
    data=pd.read_csv('Historical Price Data/'+company+'.csv')
    data['Date']=pd.to_datetime(data['Date'])
    data.index=data['Date']
    data.drop('Date',axis=1,inplace=True)
    
    data['Outstanding Shares']=0
    data.loc[data.index[len(data)-1],'Outstanding Shares']=oshares
    
    prev_index=data.index[len(data)-1]
    for index in data[:-1].index[::-1]:
        if data.loc[prev_index,'Stock Splits']!=0:
            data.loc[index,'Outstanding Shares']=data.loc[prev_index,'Outstanding Shares']/data.loc[prev_index,'Stock Splits']
        else:
            data.loc[index,'Outstanding Shares']=data.loc[prev_index,'Outstanding Shares']
        prev_index=index
    
    data.to_csv('Historical Price Data/'+company+'.csv')