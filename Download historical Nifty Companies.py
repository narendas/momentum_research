from zipfile import ZipFile
import os
import pandas as pd
import requests
import wget

os.chdir(r'C:/Users/HP/Desktop/Repos/momentum_research')
final_df=pd.DataFrame()
for files in os.listdir('Nifty Companies'):
    file=ZipFile(os.path.join('Nifty Companies',files))
    #print(file)
    try:
        df=pd.read_csv(file.open('niftymcwb.csv'))
    except:
        try:
            curr_files=files[:-4]
            df=pd.read_csv(file.open(curr_files+'/'+curr_files+'/'+'niftymcwb.csv'))
        except:
            try:
                curr_files=files[:-4]
                df=pd.read_csv(file.open(curr_files+'/'+'niftymcwb.csv'))
            except:
                try:
                    curr_files=files[:-4]
                    curr_files=curr_files[:5]+curr_files[5].capitalize()+curr_files[6:]
                    df=pd.read_csv(file.open(curr_files+'/'+'niftymcwb.csv'))
                except:
                    try:
                        df=pd.read_csv(file.open('nifty50_mcwb.csv'))
                    except:
                        try:
                            curr_files=files[:-4]
                            curr_files1=curr_files[:5]+curr_files[5].capitalize()+curr_files[6:]
                            df=pd.read_csv(file.open(curr_files+'/'+curr_files1+'/'+'niftymcwb.csv'))
                        except:
                            try:
                                curr_files=files[:-4]
                                curr_files=curr_files[:-2]+'20'+curr_files[8:]
                                df=pd.read_csv(file.open(curr_files+'/'+curr_files1+'/'+'niftymcwb.csv'))
                            except:
                                df=pd.DataFrame()
                                print(files)
    if len(df)>0:
        month=files[5:-4]    
        try:
            if month[3:]=='10' or month[3:]=='11' or month[3:]=='12' or month[3:]=='13' or month[3:]=='14':
                list1=list(df['Unnamed: 1'][3:53])
                final_df[month]=list1
            else:
                list1=list(df['Unnamed: 1'][2:52])
                final_df[month]=list1
        except:
            pass
        
final_df.to_csv('nifty_companies.csv',index=False)