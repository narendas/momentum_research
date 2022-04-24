import os
os.chdir(r'C:\Users\NarendradasT\OneDrive - Carbynetech (India ) Pvt Ltd\Desktop\Repos\momentum_research')
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import date

period='Day'
m1_tr_best=['Contrarian Strategy','L-W','1-2']
m1_itr_best=['Strategy','W-L','1-2']

m2_tr_best=['Contrarian Strategy','L-W','2-1']
m2_itr_best=['Contrarian Strategy','L-W','3-1']

m3_best=['Contrarian Strategy','L-W','3-1']

def var_historic(df):
    if isinstance(df, pd.DataFrame):
        return df.aggregate(var_historic)
    if isinstance(df, pd.Series):
        return -np.percentile(df,5)

def max_dd(df):
    previous_peaks=df.cummax()
    drawdown=(df-previous_peaks)/(previous_peaks)
    
    return drawdown.min()[0]*100

def get_stats(w,l,best_selection,momentum,portfolio,mass):
    d={}
    d_w={}
    d_l={}
    
    w_r=w.resample('M').last()
    l_r=l.resample('M').last()
    w_r=100*np.log(w_r/w_r.shift(1)).dropna()
    l_r=100*np.log(l_r/l_r.shift(1)).dropna()
    
    w_mean=w_r.mean()[0]
    l_mean=l_r.mean()[0]
    
    w_std=w_r.std()[0]
    l_std=l_r.std()[0]
    
    d_w['Momentum']=momentum
    d_w['Mass']=mass
    d_w['Strategy']=best_selection[0]
    d_w['Criterion']=best_selection[2]
    d_w['Portfolio']='W'
    
    d_w['Mean']=w_mean
    d_w['Std']=w_std
    
    d_l['Momentum']=momentum
    d_l['Mass']=mass
    d_l['Strategy']=best_selection[0]
    d_l['Criterion']=best_selection[2]
    d_l['Portfolio']='L'
    
    d_l['Mean']=l_mean
    d_l['Std']=l_std
    
    if best_selection[0]=='Strategy':
        df=w-l
        df=df.resample('M').last()
        df=100*np.log(df/df.shift(1)).dropna()
        
        mean=w_mean-l_mean
        std=df.std()[0]
        
        d['Momentum']=momentum
        d['Mass']=mass
        d['Strategy']=best_selection[0]
        d['Criterion']=best_selection[2]
        d['Portfolio']=portfolio
        
        d['Mean']=mean
        d['Std']=std
    
    elif best_selection[0]=='Contrarian Strategy':
        df=l-w
        df=df.resample('M').last()
        df=100*np.log(df/df.shift(1)).dropna()
        
        mean=l_mean-w_mean
        std=df.std()[0]
    
        
        d['Momentum']=momentum
        d['Mass']=mass
        d['Strategy']=best_selection[0]
        d['Criterion']=best_selection[2]
        d['Portfolio']=portfolio
        
        d['Mean']=mean
        d['Std']=std
    return d_w,d_l,d

def get_risks(df,best_selection,momentum,portfolio,mass):
    mdd=max_dd(df)
    
    fin=df.loc[df.index[-1],'Capital']/df.loc[df.index[0],'Capital']
    
    df=df.resample('M').last()
    df=100*np.log(df/df.shift(1)).dropna()
    mean=df.mean()[0]
    std=df.std()[0]
    
    sp=mean/std
    var=var_historic(df)[0]

    d={}
    
    d['Momentum']=momentum
    d['Mass']=mass
    d['Strategy']=best_selection[0]
    d['Criterion']=best_selection[2]
    d['Portfolio']=portfolio
    
    d['Fin Wealth']=fin
    d['Sharpe Ratio']=np.abs(sp)
    d['Var 95%']=var
    d['Max DD']=mdd
    return d
    
stats_df=pd.DataFrame(columns=['Momentum','Mass','Strategy','Criterion',
                               'Portfolio','Mean','Std'])

risks_df=pd.DataFrame(columns=['Momentum','Mass','Strategy',
                               'Criterion','Portfolio','Fin Wealth','Sharpe Ratio',
                               'Var 95%','Max DD'])
# =============================================================================
# MOMENTUM 1
# =============================================================================
'''TURNOVER RATE'''
m1_tr=pd.read_csv(os.path.join(m1_tr_best[0],'Momentum 1','Turnover Rate',m1_tr_best[1],period,m1_tr_best[2]+'.csv'),index_col='Date')
m1_tr.index=pd.to_datetime(m1_tr.index)

m1_tr_w=pd.read_csv(os.path.join(m1_tr_best[0],'Momentum 1','Turnover Rate','W',period,m1_tr_best[2]+'.csv'),index_col='Date')
m1_tr_w.index=pd.to_datetime(m1_tr_w.index)

m1_tr_l=pd.read_csv(os.path.join(m1_tr_best[0],'Momentum 1','Turnover Rate','L',period,m1_tr_best[2]+'.csv'),index_col='Date')
m1_tr_l.index=pd.to_datetime(m1_tr_l.index)

if m1_tr_best[1]=='W-L':
    d_w,d_l,d=get_stats(m1_tr_w, m1_tr_l,m1_tr_best,'Momentum 1','W-L','Turnover Rate')
    m1_tr_r=m1_tr.resample('M').last()
    m1_tr_r=100*np.log(m1_tr_r/m1_tr_r.shift(1)).dropna()
    d['Std']=m1_tr_r.std()[0]

    stats_df=pd.concat([stats_df,pd.DataFrame(d_w.values(),index=d_w.keys()).T],ignore_index=True)
    stats_df=pd.concat([stats_df,pd.DataFrame(d_l.values(),index=d_l.keys()).T],ignore_index=True)
    stats_df=pd.concat([stats_df,pd.DataFrame(d.values(),index=d.keys()).T],ignore_index=True)
    
    d=get_risks(m1_tr,m1_tr_best,'Momentum 1','W-L','Turnover Rate')
    risks_df=pd.concat([risks_df,pd.DataFrame(d.values(),index=d.keys()).T],ignore_index=True)
else:
    d_w,d_l,d=get_stats(m1_tr_w, m1_tr_l,m1_tr_best,'Momentum 1','L-W','Turnover Rate')
    m1_tr_r=m1_tr.resample('M').last()
    m1_tr_r=100*np.log(m1_tr_r/m1_tr_r.shift(1)).dropna()
    d['Std']=m1_tr_r.std()[0]
    
    stats_df=pd.concat([stats_df,pd.DataFrame(d_w.values(),index=d_w.keys()).T],ignore_index=True)
    stats_df=pd.concat([stats_df,pd.DataFrame(d_l.values(),index=d_l.keys()).T],ignore_index=True)
    stats_df=pd.concat([stats_df,pd.DataFrame(d.values(),index=d.keys()).T],ignore_index=True)
    
    d=get_risks(m1_tr,m1_tr_best,'Momentum 1','L-W','Turnover Rate')
    risks_df=pd.concat([risks_df,pd.DataFrame(d.values(),index=d.keys()).T],ignore_index=True)

'''INVERSE TURNOVER RATE'''
m1_itr=pd.read_csv(os.path.join(m1_itr_best[0],'Momentum 1','Inverse Turnover Rate',m1_itr_best[1],period,m1_itr_best[2]+'.csv'),index_col='Date')
m1_itr.index=pd.to_datetime(m1_itr.index)

m1_itr_w=pd.read_csv(os.path.join(m1_itr_best[0],'Momentum 1','Inverse Turnover Rate','W',period,m1_itr_best[2]+'.csv'),index_col='Date')
m1_itr_w.index=pd.to_datetime(m1_itr_w.index)

m1_itr_l=pd.read_csv(os.path.join(m1_itr_best[0],'Momentum 1','Inverse Turnover Rate','L',period,m1_itr_best[2]+'.csv'),index_col='Date')
m1_itr_l.index=pd.to_datetime(m1_itr_l.index)

if m1_itr_best[1]=='W-L':
    d_w,d_l,d=get_stats(m1_itr_w, m1_itr_l,m1_itr_best,'Momentum 1','W-L','Inverse Turnover Rate')
    m1_itr_r=m1_itr.resample('M').last()
    m1_itr_r=100*np.log(m1_itr_r/m1_itr_r.shift(1)).dropna()
    d['Std']=m1_itr_r.std()[0]
    
    stats_df=pd.concat([stats_df,pd.DataFrame(d_w.values(),index=d_w.keys()).T],ignore_index=True)
    stats_df=pd.concat([stats_df,pd.DataFrame(d_l.values(),index=d_l.keys()).T],ignore_index=True)
    stats_df=pd.concat([stats_df,pd.DataFrame(d.values(),index=d.keys()).T],ignore_index=True)
    
    d=get_risks(m1_itr,m1_itr_best,'Momentum 1','W-L','Inverse Turnover Rate')
    risks_df=pd.concat([risks_df,pd.DataFrame(d.values(),index=d.keys()).T],ignore_index=True)
else:
    d_w,d_l,d=get_stats(m1_itr_w, m1_itr_l,m1_itr_best,'Momentum 1','L-W','Inverse Turnover Rate')
    m1_itr_r=m1_itr.resample('M').last()
    m1_itr_r=100*np.log(m1_itr_r/m1_itr_r.shift(1)).dropna()
    d['Std']=m1_itr_r.std()[0]
    
    stats_df=pd.concat([stats_df,pd.DataFrame(d_w.values(),index=d_w.keys()).T],ignore_index=True)
    stats_df=pd.concat([stats_df,pd.DataFrame(d_l.values(),index=d_l.keys()).T],ignore_index=True)
    stats_df=pd.concat([stats_df,pd.DataFrame(d.values(),index=d.keys()).T],ignore_index=True)
    
    d=get_risks(m1_itr,m1_itr_best,'Momentum 1','L-W','Inverse Turnover Rate')
    risks_df=pd.concat([risks_df,pd.DataFrame(d.values(),index=d.keys()).T],ignore_index=True)

# =============================================================================
# MOMENTUM 2
# =============================================================================
'''TURNOVER RATE'''
m2_tr=pd.read_csv(os.path.join(m2_tr_best[0],'Momentum 2','Turnover Rate',m2_tr_best[1],period,m2_tr_best[2]+'.csv'),index_col='Date')
m2_tr.index=pd.to_datetime(m2_tr.index)

m2_tr_w=pd.read_csv(os.path.join(m2_tr_best[0],'Momentum 2','Turnover Rate','W',period,m2_tr_best[2]+'.csv'),index_col='Date')
m2_tr_w.index=pd.to_datetime(m2_tr_w.index)

m2_tr_l=pd.read_csv(os.path.join(m2_tr_best[0],'Momentum 2','Turnover Rate','L',period,m2_tr_best[2]+'.csv'),index_col='Date')
m2_tr_l.index=pd.to_datetime(m2_tr_l.index)

if m2_tr_best[1]=='W-L':
    d_w,d_l,d=get_stats(m2_tr_w, m2_tr_l,m2_tr_best,'Momentum 2','W-L','Turnover Rate')
    m2_tr_r=m2_tr.resample('M').last()
    m2_tr_r=100*np.log(m2_tr_r/m2_tr_r.shift(1)).dropna()
    d['Std']=m2_tr_r.std()[0]

    stats_df=pd.concat([stats_df,pd.DataFrame(d_w.values(),index=d_w.keys()).T],ignore_index=True)
    stats_df=pd.concat([stats_df,pd.DataFrame(d_l.values(),index=d_l.keys()).T],ignore_index=True)
    stats_df=pd.concat([stats_df,pd.DataFrame(d.values(),index=d.keys()).T],ignore_index=True)
    
    d=get_risks(m2_tr,m2_tr_best,'Momentum 2','W-L','Turnover Rate')
    risks_df=pd.concat([risks_df,pd.DataFrame(d.values(),index=d.keys()).T],ignore_index=True)
else:
    d_w,d_l,d=get_stats(m2_tr_w, m2_tr_l,m2_tr_best,'Momentum 2','L-W','Turnover Rate')
    m2_tr_r=m2_tr.resample('M').last()
    m2_tr_r=100*np.log(m2_tr_r/m2_tr_r.shift(1)).dropna()
    d['Std']=m2_tr_r.std()[0]
    
    stats_df=pd.concat([stats_df,pd.DataFrame(d_w.values(),index=d_w.keys()).T],ignore_index=True)
    stats_df=pd.concat([stats_df,pd.DataFrame(d_l.values(),index=d_l.keys()).T],ignore_index=True)
    stats_df=pd.concat([stats_df,pd.DataFrame(d.values(),index=d.keys()).T],ignore_index=True)
    
    d=get_risks(m2_tr,m2_tr_best,'Momentum 2','L-W','Turnover Rate')
    risks_df=pd.concat([risks_df,pd.DataFrame(d.values(),index=d.keys()).T],ignore_index=True)

'''INVERSE TURNOVER RATE'''
m2_itr=pd.read_csv(os.path.join(m2_itr_best[0],'Momentum 2','Inverse Turnover Rate',m2_itr_best[1],period,m2_itr_best[2]+'.csv'),index_col='Date')
m2_itr.index=pd.to_datetime(m2_itr.index)

m2_itr_w=pd.read_csv(os.path.join(m2_itr_best[0],'Momentum 2','Inverse Turnover Rate','W',period,m2_itr_best[2]+'.csv'),index_col='Date')
m2_itr_w.index=pd.to_datetime(m2_itr_w.index)

m2_itr_l=pd.read_csv(os.path.join(m2_itr_best[0],'Momentum 2','Inverse Turnover Rate','L',period,m2_itr_best[2]+'.csv'),index_col='Date')
m2_itr_l.index=pd.to_datetime(m2_itr_l.index)

if m2_itr_best[1]=='W-L':
    d_w,d_l,d=get_stats(m2_itr_w, m2_itr_l,m2_itr_best,'Momentum 2','W-L','Inverse Turnover Rate')
    m2_itr_r=m2_itr.resample('M').last()
    m2_itr_r=100*np.log(m2_itr_r/m2_itr_r.shift(1)).dropna()
    d['Std']=m2_itr_r.std()[0]
    
    stats_df=pd.concat([stats_df,pd.DataFrame(d_w.values(),index=d_w.keys()).T],ignore_index=True)
    stats_df=pd.concat([stats_df,pd.DataFrame(d_l.values(),index=d_l.keys()).T],ignore_index=True)
    stats_df=pd.concat([stats_df,pd.DataFrame(d.values(),index=d.keys()).T],ignore_index=True)
    
    d=get_risks(m2_itr,m2_itr_best,'Momentum 2','W-L','Inverse Turnover Rate')
    risks_df=pd.concat([risks_df,pd.DataFrame(d.values(),index=d.keys()).T],ignore_index=True)
else:
    d_w,d_l,d=get_stats(m2_itr_w, m2_itr_l,m2_itr_best,'Momentum 2','L-W','Inverse Turnover Rate')
    m2_itr_r=m2_itr.resample('M').last()
    m2_itr_r=100*np.log(m2_itr_r/m2_itr_r.shift(1)).dropna()
    d['Std']=m2_itr_r.std()[0]
    
    stats_df=pd.concat([stats_df,pd.DataFrame(d_w.values(),index=d_w.keys()).T],ignore_index=True)
    stats_df=pd.concat([stats_df,pd.DataFrame(d_l.values(),index=d_l.keys()).T],ignore_index=True)
    stats_df=pd.concat([stats_df,pd.DataFrame(d.values(),index=d.keys()).T],ignore_index=True)
    
    d=get_risks(m2_itr,m2_itr_best,'Momentum 2','L-W','Inverse Turnover Rate')
    risks_df=pd.concat([risks_df,pd.DataFrame(d.values(),index=d.keys()).T],ignore_index=True)
# =============================================================================
# MOMENTUM 3
# =============================================================================
m3=pd.read_csv(os.path.join(m3_best[0],'Momentum 3',m3_best[1],period,m3_best[2]+'.csv'),index_col='Date')
m3.index=pd.to_datetime(m3.index)

m3_w=pd.read_csv(os.path.join(m3_best[0],'Momentum 3','W',period,m3_best[2]+'.csv'),index_col='Date')
m3_w.index=pd.to_datetime(m3_w.index)

m3_l=pd.read_csv(os.path.join(m3_best[0],'Momentum 3','L',period,m3_best[2]+'.csv'),index_col='Date')
m3_l.index=pd.to_datetime(m3_l.index)

if m3_best[1]=='W-L':
    d_w,d_l,d=get_stats(m3_w, m3_l,m3_best,'Momentum 3','W-L','Inverse Volatility')
    m3_r=m3.resample('M').last()
    m3_r=100*np.log(m3_r/m3_r.shift(1)).dropna()
    d['Std']=m3_r.std()[0]
    
    stats_df=pd.concat([stats_df,pd.DataFrame(d_w.values(),index=d_w.keys()).T],ignore_index=True)
    stats_df=pd.concat([stats_df,pd.DataFrame(d_l.values(),index=d_l.keys()).T],ignore_index=True)
    stats_df=pd.concat([stats_df,pd.DataFrame(d.values(),index=d.keys()).T],ignore_index=True)
    
    d=get_risks(m3,m3_best,'Momentum 3','W-L','Inverse Volatility')
    risks_df=pd.concat([risks_df,pd.DataFrame(d.values(),index=d.keys()).T],ignore_index=True)
else:
    d_w,d_l,d=get_stats(m3_w, m3_l,m3_best,'Momentum 3','L-W','Inverse Volatility')
    m3_r=m3.resample('M').last()
    m3_r=100*np.log(m3_r/m3_r.shift(1)).dropna()
    d['Std']=m3_r.std()[0]
    
    stats_df=pd.concat([stats_df,pd.DataFrame(d_w.values(),index=d_w.keys()).T],ignore_index=True)
    stats_df=pd.concat([stats_df,pd.DataFrame(d_l.values(),index=d_l.keys()).T],ignore_index=True)
    stats_df=pd.concat([stats_df,pd.DataFrame(d.values(),index=d.keys()).T],ignore_index=True)
    
    d=get_risks(m3,m3_best,'Momentum 3','L-W','Inverse Volatility')
    risks_df=pd.concat([risks_df,pd.DataFrame(d.values(),index=d.keys()).T],ignore_index=True)
ticker='^NSEI'
ticker=yf.Ticker(ticker)
nifty=ticker.history(start=date(2014,1,1),end=date(2022,1,1,))
nifty=(nifty['Close']-nifty.loc[nifty.index[0],'Close'])/nifty.loc[nifty.index[0],'Close']

plot_df=pd.DataFrame()
plot_df['Momentum 1 TR']=(m1_tr-m1_tr.loc[m1_tr.index[0],'Capital'])/m1_tr.loc[m1_tr.index[0],'Capital']
plot_df['Momentum 1 ITR']=(m1_itr-m1_itr.loc[m1_itr.index[0],'Capital'])/m1_itr.loc[m1_itr.index[0],'Capital']
plot_df['Momentum 2 TR']=(m2_tr-m2_tr.loc[m2_tr.index[0],'Capital'])/m2_tr.loc[m2_tr.index[0],'Capital']
plot_df['Momentum 2 ITR']=(m2_itr-m2_itr.loc[m2_itr.index[0],'Capital'])/m2_itr.loc[m2_itr.index[0],'Capital']
plot_df['Momentum 3']=(m3-m3.loc[m3.index[0],'Capital'])/m3.loc[m3.index[0],'Capital']
plot_df['Nifty']=nifty
plot_df.plot()
