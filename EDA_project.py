# -*- coding: utf-8 -*-
"""
Created on Sat Jun 10 20:20:00 2017

@author: Jihoon_Kim
"""


# Load Modules
import numpy as np
import pandas as pd
import seaborn as sns
import dask.dataframe as dd
from dask.diagnostics import ProgressBar
pbar = ProgressBar()
pbar.register()

# Load Data
gj = dd.read_csv('./data/NHIS_OPEN_GJ_2015.CSV')
t20 = dd.read_csv('./data/NHIS_OPEN_T20_2015.CSV')
t60_part1 = dd.read_csv('./data/NHIS_OPEN_T60_2015_part1.CSV')
t60_part2 = dd.read_csv('./data/NHIS_OPEN_T60_2015_part2.CSV')
t60 = t60_part1.append(t60_part2)


# Example
sns.countplot(gj.HEIGHT.compute()) # Height Distribution