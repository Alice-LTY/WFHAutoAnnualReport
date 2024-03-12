import os
import pandas as pd

"""# carcinoma_type = "Esophagus"
"""

def Type_Group(type_code):
    squamous  = [8051, 8070, 8071, 8074, 8077, 8083] #鱗狀細胞癌
    adenocarcinoma  = [8140, 8148, 8200, 8244, 8430] #腺癌
    adeno_squamous = [8560] #腺性鱗狀癌
    others = [8000, 8010, 8013, 8020, 8145, 8246, 8255] #其它
    labels = ["鱗狀細胞癌", "腺癌", "腺性鱗狀癌"]
    hist = type_code//10

    if hist in squamous:
        return labels[0]
    if hist in adenocarcinoma:
        return labels[1]
    if hist in adeno_squamous:
        return labels[2]
    if hist in others:
        return "其他"
    return "其他（待確認）"

def Esophagus_Type_Report(df):
    df_report = df[['hist/behavior', '個案分類']]
    # df_report['hist/behavior'] = df_report['hist/behavior'].str.replace("'", '').astype(int)
    df_report = df_report[df_report['個案分類'].isin(['class1', 'class2'])]
    df_report = df_report.reset_index(drop=True)
    df_report['組織類型/性態'] = df_report['hist/behavior'].apply(Type_Group)
    order = ["鱗狀細胞癌", "腺癌", "腺性鱗狀癌", "其他", "其他（待確認）"]
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


