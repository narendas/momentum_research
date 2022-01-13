import os
os.chdir(r'C:/Users/HP/Desktop/Repos/momentum_research')
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import shapiro, normaltest, jarque_bera

from base import get_data, get_resampled_data


ticker=yf.Ticker('INFRATEL.NS')


data=get_data(ticker, start='2000-01-01')

monthly_data=get_resampled_data(ticker,start='2015-01-01',period='W')

def sampling(data,iterations,sample_size):
    sampling_data=[]
    for i in range(iterations):
        sample=np.random.choice(data,sample_size, replace=True)
        sampling_data.append(sample.mean())
    
    return np.array(sampling_data)


def sampling_corr(data,mass,velocity,iterations,sample_size):
    sampling_data=[]
    for i in range(iterations):
        sample=data.sample(sample_size,replace=True)
        corr=np.corrcoef(sample[mass],sample[velocity])[0,1]
        
        sampling_data.append(corr)
    return np.array(sampling_data)

    
print('------------------------------------Inverse Turnover Rate------------------------------------')
sampling_corr_data=sampling_corr(monthly_data,'Inverse Turnover Rate','Log Returns',5000,int(len(monthly_data)))
plt.hist(sampling_corr_data)
plt.show()
 
stat,p=shapiro(sampling_corr_data)
print('-------------------------SHAPIRO-------------------------')
print(stat,p)
if p>0.05:
    print('Guassian')
else:
    print('Not Guassian')

stat,p=normaltest(sampling_corr_data)
print('-------------------------K-squared-------------------------')
print(stat,p)
if p>0.05:
    print('Guassian')
else:
    print('Not Guassian')

stat,p=jarque_bera(sampling_corr_data)
print('-------------------------Jarque_Bera-------------------------')
print(stat,p)
if p>0.05:
    print('Guassian')
else:
    print('Not Guassian')
    


print(np.corrcoef(monthly_data['Inverse Turnover Rate'],monthly_data['Log Returns'])[0,1])

negative_returns=monthly_data[monthly_data['Log Returns']<0]
positive_returns=monthly_data[monthly_data['Log Returns']>0]

print('Positive',np.corrcoef(positive_returns['Inverse Turnover Rate'],positive_returns['Log Returns'])[0,1])
print('Negative',np.corrcoef(negative_returns['Inverse Turnover Rate'],negative_returns['Log Returns'])[0,1])


print('------------------------------------ Inverse Volatility ------------------------------------')
sampling_corr_data=sampling_corr(monthly_data,'Inverse Volatility','Log Returns',5000,int(len(monthly_data)))
plt.hist(sampling_corr_data)
plt.show()  

stat,p=shapiro(sampling_corr_data)
print('-------------------------SHAPIRO-------------------------')
print(stat,p)
if p>0.05:
    print('Guassian')
else:
    print('Not Guassian')

stat,p=normaltest(sampling_corr_data)
print('-------------------------K-squared-------------------------')
print(stat,p)
if p>0.05:
    print('Guassian')
else:
    print('Not Guassian')

stat,p=jarque_bera(sampling_corr_data)
print('-------------------------Jarque_Bera-------------------------')
print(stat,p)
if p>0.05:
    print('Guassian')
else:
    print('Not Guassian')
    


print(np.corrcoef(monthly_data['Inverse Volatility'],monthly_data['Log Returns'])[0,1])

negative_returns=monthly_data[monthly_data['Log Returns']<0]
positive_returns=monthly_data[monthly_data['Log Returns']>0]

print('Positive',np.corrcoef(positive_returns['Inverse Volatility'],positive_returns['Log Returns'])[0,1])
print('Negative',np.corrcoef(negative_returns['Inverse Volatility'],negative_returns['Log Returns'])[0,1])