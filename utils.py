import os
import pandas as pd

def create_output_directory(main_file_name, year, is_colab=True):
    """Create output directory based on the selected environment (Colab or Local)."""
    if is_colab:
        base_directory = f'/content/drive/My Drive/WFHAutoAnnualReport/{main_file_name}'
    else:
        base_directory = f'{main_file_name}'
    
    directory_path = os.path.join(base_directory, f'output{year}')
    os.makedirs(directory_path, exist_ok=True)
    
    if os.path.exists(directory_path):
        print(f"目錄 '{directory_path}' 已成功建立！")
    else:
        print(f"目錄 '{directory_path}' 建立失敗！")

    return base_directory

def clean_data(df):
    df['site'] = df['site'].str.replace("'", '')
    df['site-c'] = df['site'].str.replace("C", '').astype(int)
    df['hist/behavior'] = df['hist/behavior'].str.replace("'", '').astype(int)
    df['診斷年齡'] = df['age'].str.replace("'", '').astype(int)
    df['性別'] = "9"
    df['性別'] = df['sex'].str.replace("'1", '男')
    df['性別'] = df['性別'].str.replace("'2", '女')
    df['個案分類'] = "9"
    df['個案分類'] = df['class'].str.replace("'1", 'class1')
    df['個案分類'] = df['個案分類'].str.replace("'2", 'class2')
    df['個案分類'] = df['個案分類'].str.replace("'3", 'class3')
    df['個案分類'] = df['個案分類'].str.replace("'0", 'class0')
    df['Site'] = 1
    return df

def Site_Group_InLymphoma(site):
    if (769< site <780):
        return ("淋巴結(內)惡性淋巴癌")

def Hist_Behavior_Group(hist_):
    if ((96499< hist_ < 96680) or (96699 < hist_ < 97000) or (97609 < hist_ < 97620) or (98259 < hist_ < 98270) or (98329 < hist_ < 98340) or (99399 <hist_ < 99410) or (95959 <hist_ < 95970) or (96999 < hist_ < 97300) or (98269 < hist_ < 98280) or (97499 < hist_ < 97610) or (97639 < hist_ < 97650) or (95899 < hist_ < 95920)):
        return ("淋巴結(外)惡性淋巴瘤")

def Site_Group(site):
    if ((site < 10) or (19 <site < 24) or (27 <site < 32) or (38 <site < 42) or (47 <site < 51) or (57 <site < 63) or (67 <site < 70)):
        return ("口腔癌")
    if ((site == 19) or (site == 24) or ( 50 < site < 53) or (89 < site < 101) or (site == 104) or (107 < site < 110) or (site == 142) or (site == 148)):
        return ("口咽癌")
    if ((128 < site < 133) or (137 < site < 141)):
        return ("下咽癌")
    if ((319 < site < 330)):
        return ("喉癌")
    if (109 < site < 120):
        return ("鼻咽癌")
    if ((149 < site < 156) or (157< site < 160)):
        return ("食道癌")
    if ((159< site < 167) or (167 < site < 170)):
        return ("胃癌")
    if ((179 <site <190)):
        return ("結腸癌")
    if ((site == 199) or (site == 209)):
        return ("直腸癌")
    if (209< site < 220):
        return ("肛門癌")
    if (219< site <222):
        return ("肝癌")
    if ((249< site < 255) or (256< site< 260)):
        return ("胰臟癌")
    if ((339< site < 344) or (347 < site < 350)):
        return ("肺癌")
    if (499< site < 510):
        return ("乳癌")
    if ((529< site <532) or (537< site < 540)):
        return ("子宮頸癌")
    if ((539< site < 544) or (site == 549) or (site ==559)):
        return ("子宮體癌")
    if (site == 569):
        return ("卵巢癌")
    if (site == 619):
        return ("攝護腺癌")
    if (669< site <680):
        return ("膀胱癌")
    # if (769< site <780):
    #     return ("淋巴結(內)惡性淋巴癌")
    if (site == 421):
        return ("白血病")

    return ("其他（待確認）")

####
def Save_separated_file(df, main_file_name, year):
    cancer_types = df['Site'].unique()
    for cancer_type in cancer_types:
        subset = df[df['Site'] == cancer_type].reset_index(drop=True)
        directory_path = f'{main_file_name}/output{year}/{year}{cancer_type}'
        os.makedirs(directory_path, exist_ok=True)
        excel_file_name = f"{main_file_name}/output{year}/{year}{cancer_type}/{year}{cancer_type}.xlsx"
        csv_file_name = f"{main_file_name}/output{year}/{year}{cancer_type}/{year}{cancer_type}.csv"
        subset.to_excel(excel_file_name, index=False)
        subset.to_csv(csv_file_name, index=False)

def separate_class_of_carcinoma(df, main_file_name, year):
    df['Site'] = df['site-c'].apply(Site_Group_InLymphoma)
    condition = ((df['Site'] == '淋巴結(內)惡性淋巴癌'))
    in_lymphoma_df = df[condition]
    df.drop(df[condition].index, inplace=True)
    in_lymphoma_df = in_lymphoma_df.reset_index(drop=True)
    df = df.reset_index(drop=True)

    df['Site'] = df['hist/behavior'].apply(Hist_Behavior_Group)
    condition = ((df['Site'] == '淋巴結(外)惡性淋巴瘤'))
    ex_lymphoma_df = df[condition]
    df.drop(df[condition].index, inplace=True)
    ex_lymphoma_df = ex_lymphoma_df.reset_index(drop=True)
    df = df.reset_index(drop=True)                              # lymphoma_df, df

    df['Site'] = df['site-c'].apply(Site_Group)
    merged_df = pd.concat([in_lymphoma_df, ex_lymphoma_df], ignore_index=True)
    merged_df = pd.concat([merged_df, df], ignore_index=True)
    df = merged_df.copy()
    df = df.reset_index(drop=True)
    Save_separated_file(df, main_file_name, year)
    return df