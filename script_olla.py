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
rootDir = "..\data"
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




