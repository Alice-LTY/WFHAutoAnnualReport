"""# carcinoma_type = "Oropharynx"
carcinoma_type = "口咽癌"
"""
import os
import pandas as pd

def Type_Group(type_code):
    squamous16pos = [8070, 8072, 8083, 8085] #鱗狀細胞癌 P16+
    squamous16neg = [8051, 8052, 8070, 8074, 8075, 8082, 8083, 8086, 8560] #鱗狀細胞癌 P16-
    # others = []
    labels = ["鱗狀細胞癌 P16+", "鱗狀細胞癌 P16-"]
    hist = type_code//10

    if hist in squamous16pos:
        return labels[0]
    if hist in squamous16neg:
        return labels[1]
    return "其他（待確認）"

def Oropharynx_Type_Report(df):
    df_report = df[['hist/behavior', '個案分類']]
    # df_report['hist/behavior'] = df_report['hist/behavior'].str.replace("'", '').astype(int)
    df_report = df_report[df_report['個案分類'].isin(['class1', 'class2'])]
    df_report = df_report.reset_index(drop=True)
    df_report['組織類型/性態'] = df_report['hist/behavior'].apply(Type_Group)
    order = ["鱗狀細胞癌 P16+", "鱗狀細胞癌 P16-", "其他（待確認）"]
    _distribution = df_report['組織類型/性態'].value_counts()
    _distribution = df_report.groupby('組織類型/性態').size().reindex(order, fill_value=0).reset_index(name='count')
    _distribution['percentage'] = 1
    carcinoma_in_situ = len(df_report)-_distribution['count'][len(_distribution)-1]

    for i in range(len(_distribution)):
        _distribution['percentage'][i] = (_distribution['count'][i]/carcinoma_in_situ).round(3)
    _distribution = _distribution[_distribution['組織類型/性態'] != '其他（待確認）']
    new_row = {'組織類型/性態': '合計', 'count': carcinoma_in_situ, 'percentage': 1.00}
    _distribution.loc[len(_distribution)] = new_row
    new_row = {'組織類型/性態': '總數(含原位癌)', 'count': len(df_report), 'percentage': None}
    _distribution.loc[len(_distribution)] = new_row

    return _distribution