import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import sys
sys.path.insert(0, r"C:\Users\ali_m\AnacondaProjects\PhD\Epilepsy_Surgery_Project")

from crosstab.semiology_all_localisations import all_localisations
from crosstab.semiology_lateralisation_localisation import semiology_lateralisation_localisation
from crosstab.mega_analysis.cleaning import cleaning
from crosstab.mega_analysis.missing_columns import missing_columns
from crosstab.mega_analysis.progress_stats import progress_stats, progress_venn

def MEGA_ANALYSIS(
    excel_data = "D:\\Ali USB Backup\\1 PhD\\4. SystReview Single Table (NEW CROSSTAB) 25 July_ last.xlsx",
    n_rows = 550,
    usecols = "A:CU",
    header = 1):
    
    """
    import excel, clean data, print checks, melt and pivot_table. 

    method to lookup specific semiology with no specific index:
    df.loc[df['Semiology Category'] =='Aphasia']

    method to lookup specific semiology and paper using multiIndex: change pd.read_excel below first
    df.loc[df.loc[('Aphasia')].index.str.contains('Afif') ]

    Ali Alim-Marvasti July 2019
    """


    df = pd.read_excel(excel_data, nrows=n_rows, usecols=usecols, header=header, 
                    #index_col=[4,0]  # only if you want multi-index
                    )

    # 1. CLEANUPS: remove empty rows and columns
    print('\n1. CLEANING')
    df = cleaning(df)

    # 2. checking for missing labels e.g. Semiology Categories Labels:
    print('\n2. Checking for missing column Labels')
    missing_columns(df)
    
    # 3 ffill References:
    print('\n3. forward filling references')
    df.Reference.fillna(method='ffill', inplace=True)

    # 4 check no other entries besides "ES" and "y" in list(df['sEEG and/or ES'].unique())
    print("\n4. 'sEEG and/or ES' column only contains ['ES', nan, 'y']: ")
    print(list(df['sEEG and/or ES'].unique()) == ['ES', np.nan, 'y'])
    if not (list(df['sEEG and/or ES'].unique()) == ['ES', np.nan, 'y']):
        print('the set includes:', list(df['sEEG and/or ES'].unique()) )

    # 5. print some basic progress stats:
    print('\n\n 5. BASIC PROGRESS:')
    print('Number of articles included in this analysis:', df['Reference'].nunique())
    print('Number of patients:', df['Tot Pt included'].sum())
    print('Number of lateralising datapoints:', df.Lateralising.sum())
    print('Number of localising datapoints:', df.Localising.sum())

    df_ground_truth = progress_stats(df)
    # plot
    progress_venn(df_ground_truth, method='Lateralising')
    progress_venn(df_ground_truth, method='Localising')



    return df, df_ground_truth