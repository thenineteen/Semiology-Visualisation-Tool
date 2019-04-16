import pandas as pd
import numpy as np

def main_dataframe():
    """
    Read_excel as DataFrame in two goes and make 4 columns of equivalent MRNs.
    Returns a df with pruned columns and desired dtypes.
    
    Use this function to update the features (columns, e.g. epigastric aura)
        with binary outcomes for later classification.
    
    df_semio a subset of df used when making this function to double check types. 
    """

    excel_file = "L:\\CROSSTAB_Semiology_MDT_word.xlsx"

    df = pd.read_excel(excel_file, sheet_name = 'Test_Semiology_Crosstab', usecols="A:AM", nrows=1033)  # non-indexed

    df2 = df['Hospital No'].str.split(', ').apply(pd.Series)  # makes 4 columns of hosp no's

    # rename and make these 4 columns the MRNs, and remove old Hosp No column:
    df = df2.join(df)
    df = df.drop(['Hospital No','ILAE 1 at 1yrs but not at all yrs','count yrs','countif 1','Exclude'], axis=1)
    df.drop(df.iloc[:, 9:36], inplace=True, axis=1)  #  and drop all the f/up yrs columns from yrs 1 through to 27
    df.rename(columns={0:"MRN1", 1:"MRN2", 2:"MRN3", 3:"MRN4"}, inplace=True)

    # change the data types (bool changes NaN to True automatically so need to use fillna(False) first)
    df = df.fillna(False).astype({"IDP": object, "OP Type": 'category', "IC": bool, "Entirely Seizure-Free":bool, "ILAE 1 at 1yr":bool})

    # now get the semiology one hot encoding columns from the excel file, then join it with above:
    df_semio = pd.read_excel(excel_file, sheet_name = 'Test_Semiology_Crosstab', usecols="AN:CK", nrows=1033, dtype=float)  # non-indexed
    #df_semio = df_semio.astype(float)
    #df_semio = df_semio.replace(False, np.nan)
    df = df.join(df_semio)


    # below not required any longer.
    # now pandas df returns True each NaN entry. We need to reverse this when importing the empty excel sheet:
    # set all rows of epigastric aura to end as False
    # df.iloc[:,11:] = False

    return df, df_semio
