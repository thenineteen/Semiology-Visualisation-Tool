import pandas as pd
import numpy as np
from .semiology_all_localisations import all_localisations



def semiology_lateralisation_localisation(
    spreadsheet_path="C:\\Users\\ali_m\\Downloads\\Marvasti crosstab (2).xlsx",
    semiologies_to_extract=['Semiology'],
    localisations_to_extract=[],
    extract_lateralisation=True,
    n_rows=1000
):
    """
    Manipulate the excel spreadsheet made with Gloria to make data analysable.
    Use DataFrame, combines the semiology terms across different patients and studies.
    Imports as pd df and then melts the data and drops NANs. Then uses pivot_table with aggfunc='sum'.

    Determine which semiologies and localisations we are interested in analysing using the keywords.

    >!Check the nrows, usecols and index_col below!
    >!Check the all_localisations() function has upto date file and columns

    when you have the df, can evaluate it as such: df.loc['Hypermotor', 'FL']
    """


# set the localisations as all the anatomical columns of the excel file if not specified:
    if not localisations_to_extract:
        localisations_to_extract = all_localisations()


# load the spreadsheet with semiology and paper as multiindex:
    df_multiindex = pd.read_excel(spreadsheet_path, nrows=n_rows, usecols="A:CG", header=0, index_col=[3,0])
    df_clean = df_multiindex.dropna(axis=0, how='all')

# rename the indices to ensure we are consistent no matter what they were called in excel
    df_clean = df_clean.rename_axis(['Semiology', 'Journal Paper'])
    # if single index: df_clean.index.name = 'Semiology'

# ensure there is no index, if there is (as loaded above), then remove it:
    if type(df_clean.index) != pd.core.indexes.range.RangeIndex or type(df_clean.index) != pd.core.indexes.multi.MultiIndex:
        df_clean = df_clean.reset_index()




# name the columns for each DataFrame:
    # df_lateralisation.columns.name = "Lateralisation"
    # df_localisation.columns.name = "Localisation"

# melt the DataFrame to create a column of all the Localisation terms - to allow pivoting by Semiology
    df_melted = df_clean.melt(id_vars=semiologies_to_extract, value_vars=localisations_to_extract,
                              var_name='Localisation', value_name='numbers')

# use pivot_table() to combine the semiologies which are exactly the same:
    df_localisation = df_melted.pivot_table(index='Semiology', columns='Localisation', values='numbers', aggfunc='sum')







# # now extract the Lateralisation DataFrame
#     df_lateralisation =


    return df_localisation
