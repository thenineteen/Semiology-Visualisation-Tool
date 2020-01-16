import os
import pandas as pd

def outcomes_by_resected_lobe(directory='L:\\', filename='All_Epilepsy_Ops_CROSSTAB_Statistics_YAY_2019.xlsx',
                             lobes=['T Lx', 'T Lesx']):
    """
    Creates the list of Gold_standard post-operative ILAE 1 at all follow up years MRNs in patients who had only 
    specific lobe resections.
    
    lobes = chose from this list NBOTE THE SPACES:
    ['CCx', 'F Lesx', 'F Lesx ', 'F Lx', 'F T Lx', 'Hx', 'Hx ', 'MST', 'O Lesx', 'O Lx', 
    'O P Lx', 'P Lesx', 'P Lx', 'T F Lx', 'T Lesx', 'T Lx', 'T O Lesx', 'T P Lesx', 'T P Lx']

    These are MRNs - not exactly patients (some patients have more than one)
    """

    excel_file = os.path.join(directory, filename)
    
    df_outcomes = pd.read_excel(excel_file, sheet_name = 'Aa_E_Only_All_E_Ops_CROSSTAB', usecols=[1, 4, 36])  # non-indexed
    
    df_outcomes2 = df_outcomes['Hospital No'].str.split(', ').apply(pd.Series)  # makes 4 columns of hosp no's

    df_outcomes2.index = df_outcomes.set_index(['boolean', 'OP Type']).index  # set index (this weird line so can use deepcopy prior if req'd)

    df_outcomes3 = df_outcomes2.stack().reset_index(['boolean', 'OP Type'])  # now 1,105 non-null row DataFrame

    df_outcomes3.columns = ['Gold_outcome', 'Resected Lobe', 'MRN']  # rename columns

    df_outcomes3.set_index('MRN', inplace=True)  # now have list of 1,105 MRNs(=index) and boolean Gold_outcome as two columns in pd.DataFrame

    
    

    # from the above chose the temporal lobe resections:
    df_temporal = df_outcomes3.loc[df_outcomes3['Resected Lobe'].isin(lobes)]  # returns the rows with T Lx or T Lesx 
    

    
    
    # now to access all the Gold_outcome True from the temporal lobe resections:
    df_gold_temporal_outcomes = df_temporal.loc[df_temporal.Gold_outcome == True]  # gives a  DataFrame of all MRNs and outcome Trues
    temporal_gold_outcomes_MRNs = list(df_gold_temporal_outcomes.index.values)     # list of just MRNs for use in temporal_find_MRN_label_outcomes()
        
    # the false dataframe index values gives all temporal lobe resected patients who had surgery without gold outcome
    df_temporal_had_surgery = df_temporal.loc[df_temporal.Gold_outcome == False]
    temporal_had_surgery_MRNs = list(df_temporal_had_surgery.index.values)

    return temporal_gold_outcomes_MRNs, temporal_had_surgery_MRNs