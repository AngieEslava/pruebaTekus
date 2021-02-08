import streamlit as st
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
from ipywidgets import interact
from scipy import stats
import numpy as np

data = pd.read_csv('data.csv')
print('hecho')