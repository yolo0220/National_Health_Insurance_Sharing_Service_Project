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
plt.figure(figsize=(18, 12))
sns.countplot(x="MAIN_SICK", hue="SEX", data=t20_top10_sick)
plt.legend(["Male", "Female"])
plt.xlabel("주상병코드")
plt.show()

# MAIN_SICK / Insured CLAIM
plt.figure(figsize=(18, 12))
sns.set_color_codes("pastel")
sns.barplot(x="MAIN_SICK", y="EDEC_TRAMT", data=t20_top10_sick,
            label="보험금 총액", color="b")
sns.barplot(x="MAIN_SICK", y="EDEC_SBRDN_AMT", data=t20_top10_sick,
            label="본인 부담금", color="r")
plt.legend()
plt.xlabel("주상병코드")
plt.ylabel("평균 보험금")
plt.show()

# MAIN_SICK, SUB_SICK / HEATMAP
t20_top10_sick_with_sub_sick = t20_top10_sick.SUB_SICK.value_counts()
t20_top10_sick_with_sub_sick = t20_top10_sick_with_sub_sick[:20]
t20_main_sub_sick = t20_top10_sick[t20_top10_sick.SUB_SICK.isin(
        t20_top10_sick_with_sub_sick.index)]

plt.figure(figsize=(18, 12))
main_sub_sick_size = t20_main_sub_sick.pivot_table(index="MAIN_SICK",
                                                   columns="SUB_SICK",
                                                   aggfunc="size")
sns.heatmap(main_sub_sick_size, annot=True, fmt="d")
plt.xticks(rotation=45)
plt.title("주상병-부상병 관계")
plt.xlabel("부상병코드")
plt.ylabel("주상병코드")
plt.show()

# MAIN_SICK, SUB_SICK / HEATMAP BY CODE
t20["MAIN_SICK_CODE"] = t20.MAIN_SICK[t20.MAIN_SICK.notnull()].apply(
        lambda x: x[0])
t20["SUB_SICK_CODE"] = t20.SUB_SICK[t20.SUB_SICK.notnull()].apply(
        lambda x: x[0])

# TOP 10 MAIN_SICK, SUB_SICK BY CODE
main_sick_code_count = t20.MAIN_SICK_CODE.value_counts().compute()
top10_main_sick_code = main_sick_code_count[:10]
t20_top10_sick_code = t20[t20.MAIN_SICK_CODE.isin(
        top10_main_sick_code.index)].compute()

t20_top10_sick_with_sub_sick_code = t20_top10_sick_code.SUB_SICK_CODE.value_counts().compute()
t20_top10_sick_with_sub_sick_code = t20_top10_sick_with_sub_sick_code[:20]
t20_main_sub_sick_code = t20_top10_sick_code[t20_top10_sick_code.SUB_SICK_CODE.isin(
        t20_top10_sick_with_sub_sick_code.index)].compute()

plt.figure(figsize=(18, 12))
main_sub_sick_size_code = t20_main_sub_sick_code.pivot_table(index="MAIN_SICK_CODE",
                                                             columns="SUB_SICK_CODE",
                                                             aggfunc="size")
sns.heatmap(main_sub_sick_size_code, annot=True, fmt="d")
plt.xticks(rotation=45)
plt.title("주상병-부상병 관계")
plt.xlabel("부상병코드")
plt.ylabel("주상병코드")
plt.show()