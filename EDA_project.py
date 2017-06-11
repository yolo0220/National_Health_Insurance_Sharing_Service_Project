# -*- coding: utf-8 -*-
"""
Created on Sat Jun 10 20:20:00 2017

@author: Jihoon_Kim
"""


# Load Modules
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import dask.dataframe as dd
from dask.diagnostics import ProgressBar

# Settings
sns.set(font="NanumGothic")
pbar = ProgressBar()
pbar.register()

# Load Data
gj = dd.read_csv('./data/NHIS_OPEN_GJ_2015.CSV')  # Medical Examination Data
t20 = dd.read_csv('./data/NHIS_OPEN_T20_2015.CSV')  # Treatment Data
t60_part1 = dd.read_csv('./data/NHIS_OPEN_T60_2015_part1.CSV')
t60_part2 = dd.read_csv('./data/NHIS_OPEN_T60_2015_part2.CSV')
t60 = t60_part1.append(t60_part2)  # Prescription Data


# Count TOP 10 Main Sick
main_sick_count = t20.MAIN_SICK.value_counts().compute()
top10_main_sick = main_sick_count[:10]

# t20 table confined to top 10 main sick
t20_top10_sick = t20[t20.MAIN_SICK.isin(top10_main_sick.index)].compute()

# MAIN_SICK, SEX / COUNT
plt.figure()
sns.countplot(x="MAIN_SICK", hue="SEX", data=t20_top10_sick)
plt.legend(["Male", "Female"])
plt.show()

# MAIN_SICK / Insured CLAIM
plt.figure()
sns.set_color_codes("pastel")
sns.barplot(x="MAIN_SICK", y="EDEC_TRAMT", data=t20_top10_sick,
            label="보험금 총액", color="b")
sns.barplot(x="MAIN_SICK", y="EDEC_SBRDN_AMT", data=t20_top10_sick,
            label="본인 부담금", color="r")
plt.legend()
plt.xlabel("주상병코드")
plt.ylabel("보험금")
plt.show()

# MAIN_SICK, SUB_SICK / HEATMAP
t20_top10_sick_with_sub_sick = t20_top10_sick.SUB_SICK.value_counts()
t20_top10_sick_with_sub_sick = t20_top10_sick_with_sub_sick[:20]
t20_main_sub_sick = t20_top10_sick[t20_top10_sick.isin(
        t20_top10_sick_with_sub_sick.index)]


plt.figure()
main_sub_sick_size = t20_main_sub_sick.pivot_table(index="MAIN_SICK",
                                                   columns="SUB_SICK",
                                                   aggfunc="size")
sns.heatmap(main_sub_sick_size, annot=True, fmt='g')
plt.xticks(rotation=90)
plt.title("주상병-부상병 관계")
plt.xlabel("부상병코드")
plt.ylabel("주상병코드")
plt.show()
