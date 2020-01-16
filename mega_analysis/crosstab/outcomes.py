
import pandas as pd
import os

def gold_outcomes_MRNs(directory = 'L:\\', filename = 'All_Epilepsy_Ops_CROSSTAB_Statistics_YAY_2019.xlsx'):
    """
    Creates the list of Gold_standard post-operative ILAE 1 at all follow up years MRNs.
    Also returns had_surgery list of MRNs.

    runs as:
    gold_outcomes_MRNs, had_surgery_MRNs = gold_outcomes_MRNs()

    For use by find_MRN_label_outcomes() in json_keys_read.py

    Note this doesn't give accurate outcomes for patients with outcome 8 (no follow up data) 
        this is dealt with separately by updating the json files - see jupyter notebook:
        Semiology_Crosstab_Workflow_add_feature_values
    """
    excel_file = os.path.join(directory, filename)

    # df_outcomes_indexed = pd.read_excel(excel_file, sheet_name = 'Aa_E_Only_All_E_Ops_CROSSTAB', usecols=[1,36], index_col=0)

    # n = 0
    # gold_outcomes_MRNs = []
    # for MRN in df_outcomes_indexed.index:
    #     if df_outcomes_indexed.loc[MRN, 'boolean'].any() == True:
    #         #print (MRN)
    #         gold_outcomes_MRNs.append(MRN)
    #         n += 1
    # #print (n)  # should be 330
    # return gold_outcomes_MRNs

    ## above works but we want list of MRNs not patients: each pt may have more than one MRN.
    ## some of the MRNs in the index contain 2 or even 3 or 4 MRNs (one patient with more than one hosp no)
    ## to stack the DataFrame using all MRNs and outcomes must manipulate this DataFrame:

    df_outcomes = pd.read_excel(excel_file, sheet_name = 'Aa_E_Only_All_E_Ops_CROSSTAB', usecols=[1,36])  # non-indexed
    
    df_outcomes2 = df_outcomes['Hospital No'].str.split(', ').apply(pd.Series)  # makes 4 columns of hosp no's

    df_outcomes2.index = df_outcomes.set_index(['boolean']).index  # set index (this weird line so can use deepcopy prior if req'd)

    df_outcomes3 = df_outcomes2.stack().reset_index('boolean')  # now 1,105 non-null row DataFrame

    df_outcomes3.columns = ['Gold_outcome', 'MRN']  # rename columns

    df_outcomes3.set_index('MRN', inplace=True)  # now have list of 1,105 MRNs(=index) and boolean Gold_outcome as two columns in pd.DataFrame

    # now to access all the Gold_outcome True:
    df_gold_outcomes = df_outcomes3.loc[df_outcomes3.Gold_outcome == True]  # gives a  DataFrame of all MRNs and outcome Trues (n= 346 as repeat MRNs)
    gold_outcomes_list = list(df_gold_outcomes.index.values)     # list of just MRNs for use in find_MRN_label_outcomes()

    # the false dataframe index values gives all patients who had surgery without gold outcome
    df_had_surgery = df_outcomes3.loc[df_outcomes3.Gold_outcome == False]
    had_surgery_MRNs = list(df_had_surgery.index.values)

    return gold_outcomes_list, had_surgery_MRNs
