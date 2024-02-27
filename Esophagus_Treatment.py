"""
### 食道癌治療順序
"""
import os
import pandas as pd

def therapy_order_Esophagus(df, main_file_name, year, carcinoma_type):
    #### 資料選取
    therapy_order = ['class', 'optype_o', 'optype_h', 'rtmodal', 'ort_modal', 'srs', 'sls', 'chem_h', 'horm_h', 'immu_h', 'htep_h', 'targe_Tfacility', 'palli_h', 'other_T']
    therapy_df = df[therapy_order]
    for i in therapy_order:
        therapy_df[i] = therapy_df[i].str.replace(r"[^0-9]", '', regex=True)
        therapy_df[i] = pd.to_numeric(therapy_df[i], errors='coerce')
    therapy_df = therapy_df[therapy_df['class'].isin([1, 2])]
    therapy_df = therapy_df.reset_index()#.drop('index', axis=1)
    # therapy_df

    ########################################## "食道癌「治療」定義 " ##########################################
    # OP
    OP_df = therapy_df[~((therapy_df['optype_o'].isin([0, 99])) & (therapy_df['optype_h'].isin([0, 99])))]
    OP_df = OP_df.reset_index()#.drop('index', axis=1)
    OP_list = list(OP_df['index'])
    op = set(OP_list)
    # OP_list

    # RT
    RT_df = therapy_df[(therapy_df['rtmodal'] >= 1) & (therapy_df['rtmodal'] <= 64)]
    RT_df = RT_df.reset_index()#.drop('index', axis=1)
    RT_list = list(RT_df['index'])
    rt = set(RT_list)
    # RT_list


    # CHEM
    CHEM_df = therapy_df[(therapy_df['chem_h'] >= 1) & (therapy_df['chem_h'] <= 31)]
    CHEM_df = CHEM_df.reset_index()#.drop('index', axis=1)
    CHEM_list = list(CHEM_df['index'])
    chem = set(CHEM_list)
    # CHEM_list

    # # HORM
    # HORM_df = therapy_df[(therapy_df['horm_h'] >= 1) & (therapy_df['horm_h'] <= 31)]
    # HORM_df = HORM_df.reset_index()#.drop('index', axis=1)
    # HORM_list = list(HORM_df['index'])
    # horm = set(HORM_list)
    # HORM_list

    # IMMU
    IMMU_df = therapy_df[(therapy_df['immu_h'] >= 1) & (therapy_df['immu_h'] <= 33)]
    IMMU_df = IMMU_df.reset_index()#.drop('index', axis=1)
    IMMU_list = list(IMMU_df['index'])
    immu = set(IMMU_list)
    # IMMU_list

    # # HTEP
    # HTEP_df = therapy_df[(therapy_df['htep_h'] >= 1) & (therapy_df['htep_h'] <= 31)]
    # HTEP_df = HTEP_df.reset_index()#.drop('index', axis=1)
    # HTEP_list = list(HTEP_df['index'])
    # htep = set(HTEP_list)
    # HTEP_list

    # TARGE
    # TARGE_df = therapy_df[(therapy_df['targe_Tfacility'] >= 1) & (therapy_df['targe_Tfacility'] <= 31)]
    # TARGE_df = TARGE_df.reset_index()#.drop('index', axis=1)
    # TARGE_list = list(TARGE_df['index'])
    # tg = set(TARGE_list)
    # TARGE_list

    # PALLI
    PALLI_df = therapy_df[(therapy_df['palli_h'] >= 1) & (therapy_df['palli_h'] <= 7)]
    PALLI_df = PALLI_df.reset_index()#.drop('index', axis=1)
    PALLI_list = list(PALLI_df['index'])
    palli_therapy = set(PALLI_list)
    # PALLI_list


    # Other
    Other_df = therapy_df[(therapy_df['other_T'] >= 1) & (therapy_df['other_T'] <= 3)]
    Other_df = Other_df.reset_index()#.drop('index', axis=1)
    Other_list = list(Other_df['index'])
    other_therapy = set(Other_list)
    # Other_list

    # 同步(~非同步~)化療與放療或/與標靶治療
    sls_df = therapy_df[(therapy_df['sls'].isin([2,6]))]
    sls_df = sls_df.reset_index()#.drop('index', axis=1)
    # sls_df
    sls_list = list(sls_df['index'])
    sls = set(sls_list)
    # sls_list
    ########################################## "食道癌「治療」定義 end" ##########################################

    ########################################## "食道癌「治療」範圍" ##########################################
    #### 狄摩根規則
    result_dict = {
        "治療方式": [],
        "人數": [],
        f"{carcinoma_type} 病患 Index List": []
    }


    # 手術
    OP_therapy = list(op - (rt | chem))
    # print(f"OP_therapy:\t\t\t\t\t\t{OP_therapy}")
    result_dict["治療方式"].append("手術")
    result_dict["人數"].append(len(OP_therapy))
    result_dict[f"{carcinoma_type} 病患 Index List"].append(OP_therapy if OP_therapy else None)


    # 手術合併化療與放療
    OP_RT_CHEM_combined_therapy = list(op & rt & chem)
    # print(f"OP_RT_CHEM_combined_therapy:\t\t\t\t{OP_RT_CHEM_combined_therapy}")
    result_dict["治療方式"].append("手術合併化療與放療")
    result_dict["人數"].append(len(OP_RT_CHEM_combined_therapy))
    result_dict[f"{carcinoma_type} 病患 Index List"].append(OP_RT_CHEM_combined_therapy if OP_RT_CHEM_combined_therapy else None)


    # 手術合併放療
    OP_RT_combined_therapy = list(set(op & rt) - set(OP_RT_CHEM_combined_therapy))
    # print(f"OP_RT_combined_therapy:\t\t\t\t\t{OP_RT_combined_therapy}")
    result_dict["治療方式"].append("手術合併放療")
    result_dict["人數"].append(len(OP_RT_combined_therapy))
    result_dict[f"{carcinoma_type} 病患 Index List"].append(OP_RT_combined_therapy if OP_RT_combined_therapy else None)


    # 手術合併化療
    OP_CHEM_combined_therapy = list(set(op & chem) - set(OP_RT_CHEM_combined_therapy))
    # print(f"OP_CHEM_combined_therapy:\t\t\t\t{OP_CHEM_combined_therapy}")
    result_dict["治療方式"].append("手術合併化療")
    result_dict["人數"].append(len(OP_CHEM_combined_therapy))
    result_dict[f"{carcinoma_type} 病患 Index List"].append(OP_CHEM_combined_therapy if OP_CHEM_combined_therapy else None)

    # （非）同步 化療與放療
    chem_rt_target_indexes = set(set(chem & rt) - set(OP_RT_CHEM_combined_therapy))
    # print(f"chem_rt_target_: {chem_rt_target_indexes}")
    sync_chem_rt_target_therapy = []   # 同步化療與放療或/與標靶治療 == sls
    async_chem_rt_target_therapy = []  # 非同步化療與放療或/與標靶治療
    for i in chem_rt_target_indexes:
        if i in sls:
            sync_chem_rt_target_therapy.append(i)
        else:
            async_chem_rt_target_therapy.append(i)
    # print(f"sync_chem_rt_target_therapy:\t\t\t\t{sync_chem_rt_target_therapy}\nasync_chem_rt_target_therapy:\t\t\t\t{async_chem_rt_target_therapy}")
    result_dict["治療方式"].append("同步化療與放療或/與標靶治療")
    result_dict["人數"].append(len(sync_chem_rt_target_therapy))
    result_dict[f"{carcinoma_type} 病患 Index List"].append(sync_chem_rt_target_therapy if sync_chem_rt_target_therapy else None)


    result_dict["治療方式"].append("非同步化療與放療或/與標靶治療")
    result_dict["人數"].append(len(async_chem_rt_target_therapy))
    result_dict[f"{carcinoma_type} 病患 Index List"].append(async_chem_rt_target_therapy if async_chem_rt_target_therapy else None)


    # 放療合併化療與免疫治療
    RT_CHEM_IMMU_combined_therapy = list(rt & chem & immu)
    # print(f"RT_CHEM_IMMU_combined_therapy:\t\t\t\t{RT_CHEM_IMMU_combined_therapy}")
    result_dict["治療方式"].append("放療合併化療與免疫治療")
    result_dict["人數"].append(len(RT_CHEM_IMMU_combined_therapy))
    result_dict[f"{carcinoma_type} 病患 Index List"].append(RT_CHEM_IMMU_combined_therapy if RT_CHEM_IMMU_combined_therapy else None)


    # 放療
    RT_therapy = list(rt - (op | chem))
    # print(f"RT_therapy:\t\t\t\t\t\t{RT_therapy}")
    result_dict["治療方式"].append("放療")
    result_dict["人數"].append(len(RT_therapy))
    result_dict[f"{carcinoma_type} 病患 Index List"].append(RT_therapy if RT_therapy else None)


    # 化療合併免疫治療
    CHEM_IMMU_combined_therapy = list(set(immu & chem) - set(RT_CHEM_IMMU_combined_therapy))
    # print(f"CHEM_IMMU_combined_therapy:\t\t\t\t{CHEM_IMMU_combined_therapy}")
    result_dict["治療方式"].append("化療合併免疫治療")
    result_dict["人數"].append(len(CHEM_IMMU_combined_therapy))
    result_dict[f"{carcinoma_type} 病患 Index List"].append(CHEM_IMMU_combined_therapy if CHEM_IMMU_combined_therapy else None)


    # 化療
    chem_therapy = list(chem - (op | rt))
    # print(f"chem_therapy:\t\t\t\t\t\t{chem_therapy}")
    result_dict["治療方式"].append("化療或/與標靶治療")
    result_dict["人數"].append(len(chem_therapy))
    result_dict[f"{carcinoma_type} 病患 Index List"].append(chem_therapy if chem_therapy else None)


    # 緩和治療
    palli_therapy = list(palli_therapy)
    # print(f"palli_therapy:\t\t\t\t\t\t{palli_therapy}")
    result_dict["治療方式"].append("緩和治療")
    result_dict["人數"].append(len(palli_therapy))
    result_dict[f"{carcinoma_type} 病患 Index List"].append(palli_therapy if palli_therapy else None)


    # 其他治療
    other_therapy = list(other_therapy)
    # print(f"other_therapy:\t\t\t\t\t\t{other_therapy}")
    result_dict["治療方式"].append("其他治療")
    result_dict["人數"].append(len(other_therapy))
    result_dict[f"{carcinoma_type} 病患 Index List"].append(other_therapy if other_therapy else None)

    
    # result_dict
    result_df = pd.DataFrame(result_dict)
    # result_df

    #Save file
    result_df.to_excel(f'{main_file_name}/output{year}/{year}{carcinoma_type}/{year}{carcinoma_type}Report/{year}_{carcinoma_type}_therapy_type.xlsx', sheet_name='therapy')
    ########################################## "食道癌「治療」範圍 end" ##########################################
    return result_df
