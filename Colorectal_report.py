import os
import pandas as pd

"""# carcinoma_type = "Colon, Rectum, Anal"
"""

def Type_Group(type_code):
    squamous  = [8051, 8070, 8071, 8072, 8077, 8083, 8090] #鱗狀細胞癌
    adenocarcinoma  = [8140, 8213, 8244, 8265, 8480, 8481, 8490, 8510] #腺癌
    stomach_coma = [8936] #胃腸基質瘤
    nurv_coma = [8240, 8241, 8246, 8249] #神經內分泌瘤
    others = [8000, 8010, 8013, 8020, 8041, 8123, 8124, 8542, 8560] #其它
    labels = ["鱗狀細胞癌", "腺癌", "胃腸基質瘤", "神經內分泌瘤"]
    hist = type_code//10

    if hist in squamous:
        return labels[0]
    if hist in adenocarcinoma:
        return labels[1]
    if hist in stomach_coma:
        return labels[2]
    if hist in nurv_coma:
        return labels[3]
    if hist in others:
        return "其他"
    return "其他（待確認）"

def Colorectal_Type_Report(df):
    df_report = df[['hist/behavior', '個案分類']]
    # df_report['hist/behavior'] = df_report['hist/behavior'].str.replace("'", '').astype(int)
    df_report = df_report[df_report['個案分類'].isin(['class1', 'class2'])]
    df_report = df_report.reset_index(drop=True)
    df_report['組織類型/性態'] = df_report['hist/behavior'].apply(Type_Group)
    order = ["鱗狀細胞癌", "腺癌", "腺性鱗狀癌", "神經內分泌瘤", "其他", "其他（待確認）"]
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

