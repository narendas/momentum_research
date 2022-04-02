import os
os.chdir(r'C:/Users/NarendradasT/OneDrive - Carbynetech (India ) Pvt Ltd/Desktop/Repos/momentum_research/')
import pandas as pd
from datetime import date
import yfinance as yf
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

ticker='^NSEI'
ticker=yf.Ticker(ticker)
data=ticker.history(start=date(2014,1,1),end=date(2022,1,1))
