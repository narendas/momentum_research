import os
os.chdir(r'C:\Users\NarendradasT\OneDrive - Carbynetech (India ) Pvt Ltd\Desktop\Repos\momentum_research')
import pandas as pd
import numpy as np


def var_historic(df):
    if isinstance(df, pd.DataFrame):
        return df.aggregate(var_historic)
    if isinstance(df, pd.Series):
        return -np.percentile(df,5)

def max_dd(df):
    previous_peaks=df.cummax()
    drawdown=(df-previous_peaks)/(previous_peaks)
    
    return drawdown.min()[0]
def portfolio_chart(period):
    strategies=['Strategy','Contrarian Strategy']

    momentums=['Momentum 1','Momentum 2','Momentum 3']

    turnover_rates=['Turnover Rate']

    portfolios=['W','L','L-W','W-L']

    columns=(('Strategy','Momentum'),('Strategy','Portfolio'),
             ('Strategy','Criterion'),('Strategy','Strategy'),
             ('Summary','Mean'),('Summary','STD'),
             ('Risk Measures','Fin Wealth'),('Risk Measures','Sharpe Ratio'),
             ('Risk Measures','Var 95%'),('Risk Measures','Max DD'))
    mux=pd.MultiIndex.from_tuples(columns)
    final_df=pd.DataFrame(columns=mux)
    
    for strategy in strategies:
        for momentum in momentums:
            if momentum=='Momentum 3':
                for portfolio in portfolios:
                    
                    path=os.path.join(strategy,momentum,portfolio,period)
                    if os.path.exists(path):
                        for file in os.listdir(path):
                            
                            if strategy=='Strategy':
                                if portfolio=='W-L':
                                    d={}
                                    winner_path=os.path.join(strategy,momentum,'W',period,file)
                                    loser_path=os.path.join(strategy,momentum,'L',period,file)
                                    
                                    winner_value=pd.read_csv(winner_path,index_col=('Date'))
                                    winner_value.index=pd.to_datetime(winner_value.index)
                                    
                                    loser_value=pd.read_csv(loser_path,index_col=('Date'))
                                    loser_value.index=pd.to_datetime(loser_value.index)
                                    
                                    
                                    fin_w=winner_value.loc[winner_value.index[-1],'Capital']/winner_value.loc[winner_value.index[0],'Capital']
                                    fin_l=loser_value.loc[loser_value.index[-1],'Capital']/loser_value.loc[loser_value.index[0],'Capital']
                                    
                                    fin=fin_w-fin_l
                                    
                                    winner_value=winner_value.resample('M').last()
                                    loser_value=loser_value.resample('M').last()
                                    winner_value=100*np.log(winner_value/winner_value.shift(1)).dropna()
                                    loser_value=100*np.log(loser_value/loser_value.shift(1)).dropna()
                                    
                                    
                                    port_value=winner_value-loser_value
                                    mean_w=winner_value.mean()[0]
                                    mean_l=loser_value.mean()[0]
                                    
                                    
                                    mean=mean_w-mean_l
                                    std=port_value.std()[0]
                                    
                                    sp=mean/std
                                    var=var_historic(port_value)[0]
                                    mdd=max_dd(port_value)

                                    d[('Strategy','Momentum')]=momentum
                                    d[('Strategy','Portfolio')]='W-L'
                                    d[('Strategy','Criterion')]=file[:-4]
                                    d[('Strategy','Strategy')]=strategy
                                    
                                    d[('Summary','Mean')]=mean
                                    d[('Summary','STD')]=std
                                    
                                    d[('Risk Measures','Fin Wealth')]=fin
                                    d[('Risk Measures','Sharpe Ratio')]=sp
                                    d[('Risk Measures','Var 95%')]=var
                                    d[('Risk Measures','Max DD')]=mdd
                                    
                                else:
                                    d={}
                                    file_path=os.path.join(path,file)
                                    port_value=pd.read_csv(file_path,index_col=('Date'))
                                    port_value.index=pd.to_datetime(port_value.index)
                                    
                                    fin=port_value.loc[port_value.index[-1],'Capital']/port_value.loc[port_value.index[0],'Capital']
                                    
                                    port_value=port_value.resample('M').last()
                                    port_value=100*np.log(port_value/port_value.shift(1)).dropna()
                                    
                                    mean=port_value.mean()[0]
                                    std=port_value.std()[0]
                                    
                                    sp=mean/std
                                    var=var_historic(port_value)[0]
                                    mdd=max_dd(port_value)
                                    d[('Strategy','Momentum')]=momentum
                                    d[('Strategy','Portfolio')]=portfolio
                                    d[('Strategy','Criterion')]=file[:-4]
                                    d[('Strategy','Strategy')]=strategy
                                    
                                    d[('Summary','Mean')]=mean
                                    d[('Summary','STD')]=std
                                    
                                    d[('Risk Measures','Fin Wealth')]=fin
                                    d[('Risk Measures','Sharpe Ratio')]=sp
                                    d[('Risk Measures','Var 95%')]=var
                                    d[('Risk Measures','Max DD')]=mdd
                                    
                            
                            else:
                                if portfolio=='L-W':
                                    d={}
                                    winner_path=os.path.join(strategy,momentum,'W',period,file)
                                    loser_path=os.path.join(strategy,momentum,'L',period,file)
                                    
                                    winner_value=pd.read_csv(winner_path,index_col=('Date'))
                                    winner_value.index=pd.to_datetime(winner_value.index)
                                    
                                    loser_value=pd.read_csv(loser_path,index_col=('Date'))
                                    loser_value.index=pd.to_datetime(loser_value.index)
                                    
                                    
                                    fin_w=winner_value.loc[winner_value.index[-1],'Capital']/winner_value.loc[winner_value.index[0],'Capital']
                                    fin_l=loser_value.loc[loser_value.index[-1],'Capital']/loser_value.loc[loser_value.index[0],'Capital']
                                    
                                    fin=fin_l-fin_w
                                    
                                    
                                    winner_value=winner_value.resample('M').last()
                                    loser_value=loser_value.resample('M').last()
                                    winner_value=100*np.log(winner_value/winner_value.shift(1)).dropna()
                                    loser_value=100*np.log(loser_value/loser_value.shift(1)).dropna()
                                    
                                    
                                    port_value=loser_value-winner_value
                                    mean_w=winner_value.mean()[0]
                                    mean_l=loser_value.mean()[0]
                                    mean=mean_l-mean_w
                                    std=port_value.std()[0]
                                    
                                    sp=mean/std
                                    var=var_historic(port_value)[0]
                                    mdd=max_dd(port_value)
                                    
                                    d[('Strategy','Momentum')]=momentum
                                    d[('Strategy','Portfolio')]='L-W'
                                    d[('Strategy','Criterion')]=file[:-4]
                                    d[('Strategy','Strategy')]=strategy
                                    
                                    d[('Summary','Mean')]=mean
                                    d[('Summary','STD')]=std
                                    
                                    d[('Risk Measures','Fin Wealth')]=fin
                                    d[('Risk Measures','Sharpe Ratio')]=sp
                                    d[('Risk Measures','Var 95%')]=var
                                    d[('Risk Measures','Max DD')]=mdd
                                    
                                else:
                                    d={}
                                    file_path=os.path.join(path,file)
                                    port_value=pd.read_csv(file_path,index_col=('Date'))
                                    port_value.index=pd.to_datetime(port_value.index)
                                    
                                    fin=port_value.loc[port_value.index[-1],'Capital']/port_value.loc[port_value.index[0],'Capital']
                                    port_value=port_value.resample('M').last()
                                    port_value=100*np.log(port_value/port_value.shift(1)).dropna()
                                    
                                    mean=port_value.mean()[0]
                                    std=port_value.std()[0]
                                    
                                    sp=mean/std
                                    var=var_historic(port_value)[0]
                                    mdd=max_dd(port_value)
                                    
                                    d[('Strategy','Momentum')]=momentum
                                    d[('Strategy','Portfolio')]=portfolio
                                    d[('Strategy','Criterion')]=file[:-4]
                                    d[('Strategy','Strategy')]=strategy
                                    
                                    d[('Summary','Mean')]=mean
                                    d[('Summary','STD')]=std
                                    
                                    d[('Risk Measures','Fin Wealth')]=fin
                                    d[('Risk Measures','Sharpe Ratio')]=sp
                                    d[('Risk Measures','Var 95%')]=var
                                    d[('Risk Measures','Max DD')]=mdd
                                    
                            final_df=final_df.append(d,ignore_index=True)
            
            else:
                for turnover in turnover_rates:
                    for portfolio in portfolios:
                        
                        path=os.path.join(strategy,momentum,turnover,portfolio,period)
                        if os.path.exists(path):
                            for file in os.listdir(path):
                                if strategy=='Strategy':
                                    if portfolio=='W-L':
                                        d={}
                                        winner_path=os.path.join(strategy,momentum,turnover,'W',period,file)
                                        loser_path=os.path.join(strategy,momentum,turnover,'L',period,file)
                                        
                                        winner_value=pd.read_csv(winner_path,index_col=('Date'))
                                        winner_value.index=pd.to_datetime(winner_value.index)
                                        
                                        loser_value=pd.read_csv(loser_path,index_col=('Date'))
                                        loser_value.index=pd.to_datetime(loser_value.index)
                                        
                                        
                                        fin_w=winner_value.loc[winner_value.index[-1],'Capital']/winner_value.loc[winner_value.index[0],'Capital']
                                        fin_l=loser_value.loc[loser_value.index[-1],'Capital']/loser_value.loc[loser_value.index[0],'Capital']
                                        
                                        fin=fin_w-fin_l
                                        
                                        winner_value=winner_value.resample('M').last()
                                        loser_value=loser_value.resample('M').last()
                                        winner_value=100*np.log(winner_value/winner_value.shift(1)).dropna()
                                        loser_value=100*np.log(loser_value/loser_value.shift(1)).dropna()
                                        
                                        port_value=winner_value-loser_value
                                        mean_w=winner_value.mean()[0]
                                        mean_l=loser_value.mean()[0]
                                        
                                        mean=mean_w-mean_l
                                        std=port_value.std()[0]
                                        
                                        sp=mean/std
                                        var=var_historic(port_value)[0]
                                        mdd=max_dd(port_value)
                                        
                                        d[('Strategy','Momentum')]=momentum
                                        d[('Strategy','Portfolio')]='W-L'
                                        d[('Strategy','Criterion')]=file[:-4]
                                        d[('Strategy','Strategy')]=strategy
                                        
                                        d[('Summary','Mean')]=mean
                                        d[('Summary','STD')]=std
                                        
                                        d[('Risk Measures','Fin Wealth')]=fin
                                        d[('Risk Measures','Sharpe Ratio')]=sp
                                        d[('Risk Measures','Var 95%')]=var
                                        d[('Risk Measures','Max DD')]=mdd
                                    else:
                                        d={}
                                        file_path=os.path.join(path,file)
                                        port_value=pd.read_csv(file_path,index_col=('Date'))
                                        port_value.index=pd.to_datetime(port_value.index)
                                        
                                        fin=port_value.loc[port_value.index[-1],'Capital']/port_value.loc[port_value.index[0],'Capital']
                                        port_value=port_value.resample('M').last()
                                        port_value=100*np.log(port_value/port_value.shift(1)).dropna()
                                        
                                        mean=port_value.mean()[0]
                                        std=port_value.std()[0]
                                        
                                        sp=mean/std
                                        var=var_historic(port_value)[0]
                                        mdd=max_dd(port_value)
                                        
                                        d[('Strategy','Momentum')]=momentum
                                        d[('Strategy','Portfolio')]=portfolio
                                        d[('Strategy','Criterion')]=file[:-4]
                                        d[('Strategy','Strategy')]=strategy
                                        
                                        d[('Summary','Mean')]=mean
                                        d[('Summary','STD')]=std
                                        
                                        d[('Risk Measures','Fin Wealth')]=fin
                                        d[('Risk Measures','Sharpe Ratio')]=sp
                                        d[('Risk Measures','Var 95%')]=var
                                        d[('Risk Measures','Max DD')]=mdd
                                
                                else:
                                    if portfolio=='L-W':
                                        d={}
                                        winner_path=os.path.join(strategy,momentum,turnover,'W',period,file)
                                        loser_path=os.path.join(strategy,momentum,turnover,'L',period,file)
                                        
                                        winner_value=pd.read_csv(winner_path,index_col=('Date'))
                                        winner_value.index=pd.to_datetime(winner_value.index)
                                        
                                        loser_value=pd.read_csv(loser_path,index_col=('Date'))
                                        loser_value.index=pd.to_datetime(loser_value.index)
                                        
                                        
                                        fin_w=winner_value.loc[winner_value.index[-1],'Capital']/winner_value.loc[winner_value.index[0],'Capital']
                                        fin_l=loser_value.loc[loser_value.index[-1],'Capital']/loser_value.loc[loser_value.index[0],'Capital']
                                        
                                        fin=fin_l-fin_w
                                        
                                        winner_value=winner_value.resample('M').last()
                                        loser_value=loser_value.resample('M').last()
                                        winner_value=100*np.log(winner_value/winner_value.shift(1)).dropna()
                                        loser_value=100*np.log(loser_value/loser_value.shift(1)).dropna()
                                        
                                        port_value=loser_value-winner_value
                                        mean_w=winner_value.mean()[0]
                                        mean_l=loser_value.mean()[0]
                                        
                                        mean=mean_l-mean_w
                                        std=port_value.std()[0]
                                        
                                        sp=mean/std
                                        var=var_historic(port_value)[0]
                                        mdd=max_dd(port_value)
                                        
                                        d[('Strategy','Momentum')]=momentum
                                        d[('Strategy','Portfolio')]='L-W'
                                        d[('Strategy','Criterion')]=file[:-4]
                                        d[('Strategy','Strategy')]=strategy
                                        
                                        d[('Summary','Mean')]=mean
                                        d[('Summary','STD')]=std
                                        
                                        d[('Risk Measures','Fin Wealth')]=fin
                                        d[('Risk Measures','Sharpe Ratio')]=sp
                                        d[('Risk Measures','Var 95%')]=var
                                        d[('Risk Measures','Max DD')]=mdd
                                        
                                    else:
                                        d={}
                                        file_path=os.path.join(path,file)
                                        port_value=pd.read_csv(file_path,index_col=('Date'))
                                        port_value.index=pd.to_datetime(port_value.index)
                                        
                                        fin=port_value.loc[port_value.index[-1],'Capital']/port_value.loc[port_value.index[0],'Capital']
                                        port_value=port_value.resample('M').last()
                                        port_value=100*np.log(port_value/port_value.shift(1)).dropna()
                                        
                                        mean=port_value.mean()[0]
                                        std=port_value.std()[0]
                                        
                                        sp=mean/std
                                        var=var_historic(port_value)[0]
                                        mdd=max_dd(port_value)
                                        
                                        d[('Strategy','Momentum')]=momentum
                                        d[('Strategy','Portfolio')]=portfolio
                                        d[('Strategy','Criterion')]=file[:-4]
                                        d[('Strategy','Strategy')]=strategy
                                        
                                        d[('Summary','Mean')]=mean
                                        d[('Summary','STD')]=std
                                        
                                        d[('Risk Measures','Fin Wealth')]=fin
                                        d[('Risk Measures','Sharpe Ratio')]=sp
                                        d[('Risk Measures','Var 95%')]=var
                                        d[('Risk Measures','Max DD')]=mdd
                                        
                                final_df=final_df.append(d,ignore_index=True)
    
    return final_df


def get_best_df(df):
    #This for loop returns the best outcome out of contrarian/traditional for every j-k portfolio
    final_df=pd.DataFrame(columns=df.columns)
    for momentum in list(df[('Strategy','Momentum')].unique()):
        momentum_df=df[df[('Strategy','Momentum')]==momentum].reset_index(drop=True)
        for criterion in list(momentum_df[('Strategy','Criterion')].unique()):
            strategy_df=momentum_df[momentum_df[('Strategy','Criterion')]==criterion].reset_index(drop=True)
            w_l=strategy_df[strategy_df[('Strategy','Portfolio')]=='W-L']
            #w_l=w_l[('Summary','Mean')].item()
            w_l=w_l[('Risk Measures','Fin Wealth')].item()
            
            l_w=strategy_df[strategy_df[('Strategy','Portfolio')]=='L-W']
            #l_w=l_w[('Summary','Mean')].item()
            l_w=l_w[('Risk Measures','Fin Wealth')].item()
            
            if w_l>l_w:
                final_df=final_df.append(strategy_df[strategy_df[('Strategy','Strategy')]=='Strategy'],ignore_index=True)
            elif w_l<l_w:
                final_df=final_df.append(strategy_df[strategy_df[('Strategy','Strategy')]=='Contrarian Strategy'],ignore_index=True)

    #This for loop returns best j-k portfolio with the highest mean
    best_df=pd.DataFrame(columns=final_df.columns)
    for momentum in list(final_df[('Strategy','Momentum')].unique()):
        momentum_df=final_df[final_df[('Strategy','Momentum')]==momentum].reset_index(drop=True)
        max_strategy_df=momentum_df[momentum_df[('Strategy','Portfolio')].isin(['W-L','L-W'])].reset_index(drop=True)
        max_wealth=max_strategy_df[max_strategy_df[('Risk Measures','Fin Wealth')]==max(max_strategy_df[('Risk Measures','Fin Wealth')])].reset_index(drop=True)
        
        max_wealth=max_wealth['Strategy']['Criterion'][0]
        max_wealth=momentum_df[momentum_df[('Strategy','Criterion')]==max_wealth]
        
        best_df=best_df.append(max_wealth,ignore_index=True)
    return best_df


if __name__=='__main__':
    final_df=portfolio_chart('Month')
    best_df=get_best_df(final_df)
    best_df=best_df.groupby([('Strategy','Momentum'),('Strategy','Criterion'),('Strategy','Strategy'),('Strategy','Portfolio')]).last()