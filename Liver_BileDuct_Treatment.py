"""
### 肝癌、肝內膽管癌 治療順序
"""
import os
import pandas as pd

def therapy_order_Liver_(df):
    #### 資料選取 #### site-c 221（肝內膽管癌C22.1）
    therapy_order = ['site-c', 'class', 'optype_o', 'optype_h', 'rtmodal', 'ort_modal', 'srs', 'sls', 'chem_h', 'horm_h', 'immu_h', 'htep_h', 'targe_Tfacility', 'palli_h', 'other_T']
    therapy_df = df[therapy_order]
    for i in therapy_order:
        therapy_df[i] = therapy_df[i].str.replace(r"[^0-9]", '', regex=True)
        therapy_df[i] = pd.to_numeric(therapy_df[i], errors='coerce')
    therapy_df = therapy_df[therapy_df['class'].isin([1, 2])]
    liver_cancer_df = therapy_df[therapy_df['site-c'] != 221]
    bile_duct_cancer_df = therapy_df[therapy_df['site-c'] == 221]
    liver_cancer_df = liver_cancer_df.reset_index()
    bile_duct_cancer_df = bile_duct_cancer_df.reset_index()    
    # therapy_df = therapy_df.reset_index()#.drop('index', axis=1)

    ########################################## "肝癌「治療」定義 " ##########################################
    del therapy_df
    therapy_df = liver_cancer_df.copy()

    # OP\Transplant(tp)\Transcatheter(tc)
    OP_df = therapy_df[~((therapy_df['optype_o'].isin([0, 99])) & (therapy_df['optype_h'].isin([0, 99]))) & (~therapy_df['optype_o'].isin([61, 75, 15]))]
    OP_df = OP_df.reset_index()#.drop('index', axis=1)
    op_general = set(OP_df['index'])

    transplant_df = therapy_df[(therapy_df['optype_o'].isin([61, 75]))]
    transplant_df = transplant_df.reset_index()
    tp = set(transplant_df['index'])

    transcatheter_df = therapy_df[(therapy_df['optype_o'].isin([15]))]
    transcatheter_df = transcatheter_df.reset_index()
    tc = set(transcatheter_df['index'])

    # RT
    RT_df = therapy_df[(therapy_df['rtmodal'] >= 1) & (therapy_df['rtmodal'] <= 64)]
    RT_df = RT_df.reset_index()#.drop('index', axis=1)
    rt = set(RT_df['index'])

    # CHEM
    CHEM_df = therapy_df[(therapy_df['chem_h'] >= 4) & (therapy_df['chem_h'] <= 7)]
    CHEM_df = CHEM_df.reset_index()#.drop('index', axis=1)
    chem_local = set(CHEM_df['index'])

    CHEM_df = therapy_df[(therapy_df['chem_h'] >= 0) & (therapy_df['chem_h'] <= 31)]
    CHEM_df = CHEM_df.reset_index()#.drop('index', axis=1)
    chem_general = set(CHEM_df['index'])

    # IMMU
    IMMU_df = therapy_df[(therapy_df['immu_h'] >= 4) & (therapy_df['immu_h'] <= 7)]
    IMMU_df = IMMU_df.reset_index()#.drop('index', axis=1)
    immu_local = set(IMMU_df['index'])

    IMMU_df = therapy_df[(therapy_df['immu_h'] >= 0) & (therapy_df['immu_h'] <= 31)]
    IMMU_df = IMMU_df.reset_index()#.drop('index', axis=1)
    immu_general = set(IMMU_df['index'])

    # TARGE
    TARGE_df = therapy_df[(therapy_df['targe_Tfacility'] >= 1) & (therapy_df['targe_Tfacility'] <= 31)]
    TARGE_df = TARGE_df.reset_index()#.drop('index', axis=1)
    tg = set(TARGE_df['index'])

    # PALLI
    PALLI_df = therapy_df[(therapy_df['palli_h'] >= 1) & (therapy_df['palli_h'] <= 7)]
    PALLI_df = PALLI_df.reset_index()#.drop('index', axis=1)
    palli_therapy = set(PALLI_df['index'])

    # Other
    Other_df = therapy_df[(therapy_df['other_T'] >= 1) & (therapy_df['other_T'] <= 3)]
    Other_df = Other_df.reset_index()#.drop('index', axis=1)
    other_therapy = set(Other_df['index'])
    
    # 同步(~非同步~)化療與放療或/與標靶治療
    sls_df = therapy_df[(therapy_df['sls'].isin([2,6]))]
    sls_df = sls_df.reset_index()#.drop('index', axis=1)
    sls = set(sls_df['index'])
    ########################################## "肝癌「治療」定義 end" ##########################################

    ########################################## "肝癌「治療」範圍" ##########################################
    therapy_types = {
    "手術": op_general - (chem_local),
    "肝移植": tp,
    "栓塞": tc,
    "局部治療": chem_local & immu_local,
    "手術合併局部治療": op_general & chem_local & immu_local, 
    # "手術合併栓塞": 無法篩選,
    "手術合併標靶治療"
    "局部治療合併栓塞"
    "栓塞合併標靶治療"
    "放療合併栓塞"
    "放療合併栓塞與標靶治療"
    "化療"
    "化療合併標靶治療"
    "放療合併標靶治療"
    "標靶治療"
    "免疫治療"
    "免疫治療合併標靶治療"
    "緩和治療": palli_therapy,
    "其他治療": other_therapy
    }


    #
    OP_TC_combined_therapy = list(set())
    result_dict["治療方式"].append("手術合併栓塞")
    result_dict["人數"].append(len(OP_TC_combined_therapy))
    result_dict[f"{carcinoma_type} 病患 Index List"].append(OP_TC_combined_therapy if OP_TC_combined_therapy else None)

    #手術合併標靶治療
    OP_TP_combined_therapy = list(set(op & tp))
    result_dict["治療方式"].append("手術合併標靶治療")
    result_dict["人數"].append(len(OP_TP_combined_therapy))
    result_dict[f"{carcinoma_type} 病患 Index List"].append(OP_TP_combined_therapy if OP_TP_combined_therapy else None)


    # 局部治療合併栓塞
    TC_CHEM_local_combined_therapy = list(set(tc & chem_local))
    result_dict["治療方式"].append("局部治療合併栓塞")
    result_dict["人數"].append(len(TC_CHEM_local_combined_therapy))
    result_dict[f"{carcinoma_type} 病患 Index List"].append(TC_CHEM_local_combined_therapy if TC_CHEM_local_combined_therapy else None)

    # 標靶治療
    TG_therapy = list(tg - (op | tc | rt | chem_general | immu))
    result_dict["治療方式"].append("標靶治療")
    result_dict["人數"].append(len(tg_therapy))
    result_dict[f"{carcinoma_type} 病患 Index List"].append(tg_therapy if tg_therapy else None)


    # 栓塞合併標靶治療
    TC_TG_combined_therapy = list(set(tc & tg) - set(rt & tc & tg))
    result_dict["治療方式"].append("栓塞合併標靶治療")
    result_dict["人數"].append(len(TC_TG_combined_therapy))
    result_dict[f"{carcinoma_type} 病患 Index List"].append(TC_TG_combined_therapy if TC_TG_combined_therapy else None)

    # 放療合併栓塞
    TC_RT_combined_therapy = list(set(tc & rt) - set(rt & tc & tg))
    result_dict["治療方式"].append("放療合併栓塞")
    result_dict["人數"].append(len(TC_RT_combined_therapy))
    result_dict[f"{carcinoma_type} 病患 Index List"].append(TC_RT_combined_therapy if TC_RT_combined_therapy else None)


    # 化療
    CHEM_therapy = list(chem_general - tg)
    result_dict["治療方式"].append("化療")
    result_dict["人數"].append(len(CHEM_therapy))
    result_dict[f"{carcinoma_type} 病患 Index List"].append(CHEM_therapy if CHEM_therapy else None)


    # 化療合併標靶治療
    CHEM_TG_combined_therapy = list(set(chem_general & tg))
    result_dict["治療方式"].append("化療合併標靶治療")
    result_dict["人數"].append(len(CHEM_TG_combined_therapy))
    result_dict[f"{carcinoma_type} 病患 Index List"].append(CHEM_TG_combined_therapy if CHEM_TG_combined_therapy else None)


    # 免疫治療
    IMMU_therapy = list(immu - tg)
    result_dict["治療方式"].append("免疫治療")
    result_dict["人數"].append(len(IMMU_therapy))
    result_dict[f"{carcinoma_type} 病患 Index List"].append(IMMU_therapy if IMMU_therapy else None)


    # 化療合併標靶治療
    IMMU_TG_combined_therapy = list(set(immu & tg))
    result_dict["治療方式"].append("化療合併標靶治療")
    result_dict["人數"].append(len(IMMU_TG_combined_therapy))
    result_dict[f"{carcinoma_type} 病患 Index List"].append(IMMU_TG_combined_therapy if IMMU_TG_combined_therapy else None)



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
    ########################################## "肝癌「治療」範圍 end" ##########################################
    return result_df


