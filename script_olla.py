# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 19:19:25 2021

@author: devuser
"""

import pandas as pd
import os
import sys
from os import listdir
from os.path import isfile, isdir, join
from datetime import datetime, timedelta
from pandas import DataFrame
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
#%%
# ".\ciudades.csv"
n = 0
rootDir = r"C:\cursoDataScience\data"
data_clean = pd.DataFrame()

for dirName, subdirList, fileList in os.walk(rootDir):
    n += 1
    print(n,'Directorio encontrado: %s' % dirName)
    for fname in fileList:
        print('\t%s' % fname)    
        path = dirName+'\\'+fname
        df = pd.read_csv(path)
        data_clean = data_clean.append(df , ignore_index=True)
        #, ignore_index=True
#Tomado de: https://stackoverflow.com/questions/32363154/reading-multiple-csv-files-from-multiple-files-into-pandas-dataframe
#%%
data = data_clean.copy(deep=False)
data = data.drop([ 'HardwareInteractions','StandardInteractions', 'TenantId' , 'SessionId','Id', 'DateInTicks', 'TTL'], axis=1)
data[['Fecha','Hora']] = data.Date.str.split("T",expand=True)
data = data.drop(['Hora'],axis=1)
data
#%%
#filtro de ceros
df_city =  pd.read_csv(r"C:\cursoDataScience\ciudades.csv")
df =  pd.merge(left = data, right = df_city, left_on='Key', right_on='Key')
df = df.drop(['idCity'],axis=1)
top_city = top_city.groupby('City').sum().sort_values('MovementInteractions', ascending=False).head(10)
#%%
df_mi = df[df['MovementInteractions'] != 0]
df_md = df[df['MovementDuration'] != 0]
boxplot = df_mi.boxplot(column=[  'MovementInteractions'])
boxplot = df_md.boxplot(column=['MovementDuration'])
key = df.loc[:, 'Key'] 
key.drop_duplicates(inplace=True)

sns.catplot(x="Key", y="MovementDuration", data=df_md).fig.set_size_inches(15,5) #https://stackoverflow.com/questions/33446029/how-to-change-a-figures-size-in-python-seaborn-package
plt.xticks([r for r in range(len(key))] , key.index, rotation = 'vertical')

sns.catplot(x="Key", y="MovementDuration", data=df).fig.set_size_inches(15,5) #https://stackoverflow.com/questions/33446029/how-to-change-a-figures-size-in-python-seaborn-package
plt.xticks([r for r in range(len(key))] , key.index, rotation = 'vertical')

sns.catplot(x="Key", y="MovementInteractions", jitter=False, data=df_mi).fig.set_size_inches(15,5)
plt.xticks([r for r in range(len(key))] , key.index, rotation = 'vertical')

#%%
df_mi.groupby('Date').MovementInteractions.sum().plot.line()

#para saber la cantidad de atipiocos en el conjunto de datos
#df[np.abs(stats.zscore(df['ArkboxInteractions'])) > 3]