import os
import pandas as pd

def Semiology_Crosstab_exclude_files_with_outcome_8(
    directory='L:\\', filename='CROSSTAB_Semiology_MDT_word.xlsx'
                             ):
    """
    Creates the list of MRNs which should be excluded from the analysis as they had no data (ILAE outcome 8 at year 1).    
    These are MRNs - not exactly patients (some patients have more than one)
    """

    excel_file = os.path.join(directory, filename)
    
    df_outcomes = pd.read_excel(excel_file, sheet_name = 'Test_Semiology_Crosstab', usecols=[1, 6])  # non-indexed
    
    df_outcomes2 = df_outcomes['Hospital No'].str.split(', ').apply(pd.Series)  # makes 4 columns of hosp no's

    df_outcomes2.index = df_outcomes.set_index(['Exclude']).index  # set index (this weird line so can use deepcopy prior if req'd)

    df_outcomes3 = df_outcomes2.stack().reset_index(['Exclude'])  # now 1,105 non-null row DataFrame

    df_outcomes3.columns = ['Exclude', 'MRN']  # rename columns

    df_outcomes3.set_index('MRN', inplace=True)  # now have list of 1,105 MRNs(=index) and boolean Exclude criteria in pd.DataFrame

    
    
    
    
    # now to access all the Excludes:
    df_exclude = df_outcomes3.loc[df_outcomes3.Exclude == True]  # gives a  DataFrame of all MRNs and Exclude Trues
    Exclude_no_outcomes_MRNs = list(df_exclude.index.values)     # list of just MRNs for use in temporal_find_MRN_label_outcomes()
        
 
    return Exclude_no_outcomes_MRNs