import pandas as pd
import os

# # 各癌別

def Age_Group(age):
    bins = [40, 50, 60, 70, 80]
    labels = ['≦39', '40-49', '50-59', '60-69', '70-79', '≧80']

    for i in range(len(bins)):
        if age < bins[i]:
            return labels[i]

    return labels[-1]

def Age_Gender_Report(df):
    df_report = df[['診斷年齡', '性別']]
    df_report['年齡區間'] = df_report['診斷年齡'].apply(Age_Group)
    # df_report
    order = ['≦39', '40-49', '50-59', '60-69', '70-79', '≧80']
    cross_table = pd.crosstab(df_report['性別'], df_report['年齡區間'], margins=True, margins_name='總計')
    cross_table = cross_table.reindex(columns=order)
    cross_table['總計'] = cross_table.sum(axis=1)
    # cross_table
    percentage_table = cross_table.div(cross_table['總計'], axis=0) * 100
    percentage_table = percentage_table.round(1)
    # percentage_table
    total_percentage = [percentage_table.xs('總計')]
    # list(total_percentage[0])
    cross_table.loc['總計百分比'] = list(total_percentage[0])
    return cross_table, df_report

####
def Class_Gender_Report(df):
    df_report = df[['個案分類', '性別']]
    # df_report
    order = ['class0', 'class1', 'class2', 'class3']
    cross_table = pd.crosstab(df_report['性別'], df_report['個案分類'], margins=True, margins_name='總計')
    cross_table = cross_table.reindex(columns=order)
    cross_table['總計'] = cross_table.sum(axis=1)
    # Fill missing values with 0
    cross_table = cross_table.fillna(0)
    # cross_table
    percentage_table = cross_table.div(cross_table['總計'], axis=0) * 100
    percentage_table = percentage_table.round(1)
    # percentage_table
    total_percentage = [percentage_table.xs('總計')]
    # list(total_percentage[0])
    cross_table.loc['總計百分比'] = list(total_percentage[0])
    return cross_table, df_report


####
def clean(df):
    df_AJCC_stage = df[['class', 'pdescr', 'pstage', 'cstage']]
    df_AJCC_stage['class'] = df_AJCC_stage['class'].str.replace("'", '').astype(int)
    df_AJCC_stage = df_AJCC_stage[df_AJCC_stage['class'].isin([1, 2])]
    df_AJCC_stage = df_AJCC_stage.reset_index(drop=True)
    df_AJCC_stage['pdescr'] = df_AJCC_stage['pdescr'].str.replace("'", '').astype(int)
    df_AJCC_stage['pstage'] = df_AJCC_stage['pstage'].str.replace("'", '') #str
    df_AJCC_stage['cstage'] = df_AJCC_stage['cstage'].str.replace("'", '') #str
    return df_AJCC_stage


def to_define_stage(df_AJCC_stage, i):
    if (df_AJCC_stage['pdescr'][i] in [4, 6]):
        return df_AJCC_stage['cstage'][i]
    if (df_AJCC_stage['pstage'][i] in ["999", "888", "BBB"]):
        return df_AJCC_stage['cstage'][i]
    return df_AJCC_stage['pstage'][i]

def Define_Stage_(df):
    df_AJCC_stage = clean(df)
    df_AJCC_stage['STAGE'] = None
    for i in range (len(df_AJCC_stage)):
        df_AJCC_stage['STAGE'][i] = to_define_stage(df_AJCC_stage, i)
    return df_AJCC_stage


def Distribution_tabel(order, df_AJCC_stage, main_file_name, year, carcinoma_type):
    _distribution = df_AJCC_stage['STAGE'].value_counts()
    _distribution = df_AJCC_stage.groupby('STAGE').size().reindex(order, fill_value=0).reset_index(name='count')
    sum_counts = _distribution.loc[_distribution['STAGE'].isin(['BBB', '888', '999']), 'count'].sum()
    _distribution = _distribution[~_distribution['STAGE'].isin(['BBB', '888', '999'])]
    new_row = pd.DataFrame([{'STAGE': '不詳期別', 'count': sum_counts}])
    _distribution = pd.concat([_distribution, new_row], ignore_index=True)
    _distribution.to_excel(f'{main_file_name}/output{year}/{year}{carcinoma_type}/{year}{carcinoma_type}Report/{year}_{carcinoma_type}_AJCC_stage.xlsx', sheet_name='AJCC_stage')
    return _distribution


