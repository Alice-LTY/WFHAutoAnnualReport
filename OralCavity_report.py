"""# carcinoma_type = "OralCavity"
carcinoma_type = "口腔癌"
"""
import os
import pandas as pd

def Type_Group(type_code):
    squamous = [8051, 8052, 8070, 8071, 8072, 8074, 8075, 8082, 8083] #鱗狀細胞癌
    others = [8140, 8147, 8200, 8290, 8310, 8430, 8500, 8525.8550, 8560, 8562, 8982] #其他
    labels = ["鱗狀細胞癌", "其他"]
    hist = type_code//10

    if hist in squamous:
        return labels[0]
    if hist in others:
        return "其他"
    return "其他（待確認）"

def Type_Report(df):
    df_report = df[['hist/behavior', '個案分類']]
    # df_report['hist/behavior'] = df_report['hist/behavior'].str.replace("'", '').astype(int)
    df_report = df_report[df_report['個案分類'].isin(['class1', 'class2'])]
    df_report = df_report.reset_index(drop=True)
    df_report['組織類型/性態'] = df_report['hist/behavior'].apply(Type_Group)
    order = ["鱗狀細胞癌", "其他", "其他（待確認）"]
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

# 頰部 C06.0-C06.2  C06.8-C06.9
# 舌部 C02.0-C02.3 C02.8-C02.9
# 牙齦 C03.0-C03.1 C03.9
# 唇部 C00.0-C00.9
# 口底 C040-C041 C04.8-C04.9
# 硬顎 C05.0  C05.8-C05.9
def insite(site_org):
    Cheek = [60, 61, 62, 68, 69]
    Tongue  = [20, 21, 22, 23, 28, 29]
    Gingiva = [30, 31, 39]
    Lips = [i for i in range(0, 10)]
    Floor_of_mouth = [40, 41, 48, 49]
    Hard_palate = [50, 58, 5.9]

    if site_org in Cheek:
        return "頰部"
    if site_org in Tongue:
        return "舌部"
    if site_org in Gingiva:
        return "牙齦"
    if site_org in Lips:
        return "唇部"
    if site_org in Floor_of_mouth:
        return "口底"
    if site_org in Hard_palate:
        return "硬顎"
    else:
        return None


def oral_in_site_(df, main_file_name, year, carcinoma_type):
    df_site_distribution = df[['site-c', 'class']]
    df_site_distribution['class'] = df_site_distribution['class'].str.replace("'", '').astype(int)
    for i in range(len(df_site_distribution)):
        if int(df_site_distribution["class"][i]) not in range(0, 4):
            df_site_distribution = df_site_distribution.drop(df_site_distribution.columns[i], axis=1)

    df_site_distribution["site"] = None
    df_site_distribution["site"] = df_site_distribution["site-c"].apply(insite)
    site_distribution_ = df_site_distribution["site"].value_counts()
    site_distribution_ = pd.DataFrame(site_distribution_)
    
    #Save file
    site_distribution_.to_excel(f'{main_file_name}/output{year}/{year}{carcinoma_type}/{year}{carcinoma_type}Report/{year}_{carcinoma_type}_口腔癌原發部位.xlsx', sheet_name='site_class')
    return site_distribution_