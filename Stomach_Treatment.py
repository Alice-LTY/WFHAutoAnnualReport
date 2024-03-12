"""
### 胃癌治療順序
"""
import os
import pandas as pd

def therapy_order_Stomach(df, main_file_name, year, carcinoma_type):
    #### 資料選取
    therapy_order = ['class', 'optype_o', 'optype_h', 'rtmodal', 'ort_modal', 'srs', 'sls', 'chem_h', 'horm_h', 'immu_h', 'htep_h', 'targe_Tfacility', 'palli_h', 'other_T']
    therapy_df = df[therapy_order]
    for i in therapy_order:
        therapy_df[i] = therapy_df[i].str.replace(r"[^0-9]", '', regex=True)
        therapy_df[i] = pd.to_numeric(therapy_df[i], errors='coerce')
    therapy_df = therapy_df[therapy_df['class'].isin([1, 2])]
    therapy_df = therapy_df.reset_index()#.drop('index', axis=1)
    # therapy_df

    ########################################## "胃癌「治療」定義 " ##########################################
    # OP
    OP_df = therapy_df[~((therapy_df['optype_o'].isin([0, 99])) & (therapy_df['optype_h'].isin([0, 99])))]
    OP_df = OP_df.reset_index()#.drop('index', axis=1)
    op = set(OP_df['index'])

    # RT
    RT_df = therapy_df[(therapy_df['rtmodal'] >= 1) & (therapy_df['rtmodal'] <= 64)]
    RT_df = RT_df.reset_index()#.drop('index', axis=1)
    rt = set(RT_df['index'])

    # CHEM
    CHEM_df = therapy_df[(therapy_df['chem_h'] >= 1) & (therapy_df['chem_h'] <= 31) & (therapy_df['chem_h'] != 9)]
    CHEM_df = CHEM_df.reset_index()#.drop('index', axis=1)
    chem_general = set(CHEM_df['index'])

    CHEM_df = therapy_df[(therapy_df['chem_h'] == 9)]
    CHEM_df = CHEM_df.reset_index()#.drop('index', axis=1)
    chem_local = set(CHEM_df['index'])

    CHEM_df = therapy_df[(therapy_df['chem_h'] >= 1) & (therapy_df['chem_h'] <= 31)]
    CHEM_df = CHEM_df.reset_index()#.drop('index', axis=1)
    chem = set(CHEM_df['index'])

    # IMMU
    IMMU_df = therapy_df[(therapy_df['immu_h'] >= 1) & (therapy_df['immu_h'] <= 33)]
    IMMU_df = IMMU_df.reset_index()#.drop('index', axis=1)
    immu = set(IMMU_df['index'])
    
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
    sls_df = sls_df.reset_index()
    sls = set(sls_df['index'])
    ########################################## "胃癌「治療」定義 end" ##########################################

    ########################################## "胃癌「治療」範圍" ##########################################
    therapy_types = {
    "手術": op - (rt | chem | tg),
    "手術合併化療": (op & chem_general) - (op & chem & rt),
    "手術合併全申身與局部化療": (op & chem_local) - (op & chem  & rt),
    "手術合併化療與放療": op & rt & chem,
    "手術合併標靶治療": op & tg,
    "手術合併化療與免疫治療": op & immu & chem,
    "同步化療與放療或": sls & ((chem & rt) - (op & rt & chem)),
    "非同步化療與放療或": ((chem & rt) - (op & rt & chem )) - (sls & ((chem & rt) - (op & rt & chem))),
    "放療": rt - (op | chem),
    "化療合併免疫治療": (immu & chem) - (op & chem & immu),
    "化療": chem - (op | rt | immu),
    "標靶治療": tg - (tg & op),
    "緩和治療": palli_therapy,
    "其他治療": other_therapy
    }
    other_therapy_indices = set(range(len(df))) - set().union(*[therapy_index_set for therapy_index_set in therapy_types.values()])
    other_therapy_indices = sorted(list(other_therapy_indices))
    therapy_types["無法歸類為上述治療方式"] = other_therapy_indices

    # Create a list to store the classification for each case
    classification_list = []

    # Create a dictionary to store the count of each therapy type
    therapy_count = {therapy_name: 0 for therapy_name in therapy_types}

    # Classify each case
    for therapy_name, therapy_index_set in therapy_types.items():
        indices = sorted(list(therapy_index_set))
        therapy_count[therapy_name] = len(indices)
        classification_list.append({"治療方式": therapy_name, f"{carcinoma_type} 病患 Index List": indices, "人數": len(indices)})

    # Convert the list to a DataFrame
    result_df = pd.DataFrame(classification_list)

    # Add a new column for the count of each therapy type
    result_df["人數"] = result_df["治療方式"].map(therapy_count)

    #Save file
    result_df.to_excel(f'{main_file_name}/output{year}/{year}{carcinoma_type}/{year}{carcinoma_type}Report/{year}_{carcinoma_type}_therapy_type.xlsx', sheet_name='therapy')
    ########################################## "胃癌「治療」範圍 end" ##########################################
    return result_df