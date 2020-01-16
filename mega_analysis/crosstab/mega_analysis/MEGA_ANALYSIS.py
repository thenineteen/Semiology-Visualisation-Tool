import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import sys
sys.path.insert(0, r"C:\Users\ali_m\AnacondaProjects\PhD\Epilepsy_Surgery_Project")

from ..semiology_all_localisations import all_localisations
from ..semiology_lateralisation_localisation import semiology_lateralisation_localisation
from ..mega_analysis.cleaning import cleaning
from ..mega_analysis.missing_columns import missing_columns
from ..mega_analysis.progress_stats import progress_stats, progress_venn
from ..mega_analysis.progress_study_type import progress_study_type, progress_venn_2
from ..mega_analysis.exclusions import exclusions



def MEGA_ANALYSIS(
        excel_data="D:\\Ali USB Backup\\1 PhD\\4. SystReview Single Table (NEW CROSSTAB) 25 July_ last.xlsx",
        n_rows=550,
        usecols="A:CU",
        header=1,
        exclude_data=False,
        plot=False,
        **kwargs,
        ):

    """
    import excel, clean data, print checks, melt and pivot_table.
    exclude_data > see exclusions.
    kwargs can be one of the exclusion keywords to pass on to exclusions.
        POST_ictals=True,
        PET_hypermetabolism=True,
        SPECT_PET=False,
        CONCORDANCE=False

    method to lookup specific semiology with no specific index:
    df.loc[df['Semiology Category'] =='Aphasia']

    method to lookup specific semiology and paper using multiIndex: change pd.read_excel below first
    df.loc[df.loc[('Aphasia')].index.str.contains('Afif') ]

    Ali Alim-Marvasti July Aug 2019
    """


    df = pd.read_excel(excel_data, nrows=n_rows, usecols=usecols, header=header,
                    #index_col=[4,0]  # only if you want multi-index
                    )


    # 0. CLEANUPS: remove empty rows and columns
    print('\n0. DataFrame pre-processing and cleaning:')
    df = cleaning(df)

    # 1. Exclusions
    if exclude_data:
        print('\n\n1. Excluding some data based on ground truths')
        if not kwargs:
            df = exclusions(df,
                POST_ictals=True,
                PET_hypermetabolism=True,
                SPECT_PET=False,
                CONCORDANCE=False)
        elif kwargs:
            df = exclusions(df,
                POST_ictals=kwargs['POST_ictals'],
                PET_hypermetabolism=kwargs['PET_hypermetabolism'],
                SPECT_PET=kwargs['SPECT_PET'],
                CONCORDANCE=kwargs['CONCORDANCE'])

        print('\ndf.shape after exclusions: ', df.shape)
    else:
        print('1. No Exclusions.')

    # 2. checking for missing labels e.g. Semiology Categories Labels:
    print('\n2. Checking for missing values for columns')
    missing_columns(df)
    print('\n Checking for dtypes:')
    localisation_labels = df.columns[17:72]
    for col in df[localisation_labels]:
        for val in df[col]:
            if ( type(val) != (np.float) ) & ( type(val) != (np.int) ):
                print(type(val), col, val)

    # 3 ffill References:
    df.Reference.fillna(method='ffill', inplace=True)
    print('\n3. forward filled references')

    # 4 check no other entries besides "ES" and "y" in list(df['sEEG and/or ES'].unique())
    print("\n4. 'sEEG and/or ES' column only contains ['ES', nan, 'y']: ")
    print(list(df['sEEG and/or ES'].unique()) == ['ES', np.nan, 'y'])
    if not (list(df['sEEG and/or ES'].unique()) == ['ES', np.nan, 'y']):
        print('the set includes:', list(df['sEEG and/or ES'].unique()) )

    # 5. print some basic progress stats:
    print('\n\n 5. BASIC PROGRESS:')
    print('Number of articles included in this analysis:', int( df['Reference'].nunique()) )
    print('Number of patients:', int( df['Tot Pt included'].sum()) )
    print('Number of lateralising datapoints:', df.Lateralising.sum())
    print('Number of localising datapoints:', df.Localising.sum())

    df_ground_truth = progress_stats(df)

    # plot progress by ground truth
    if plot:
        progress_venn(df_ground_truth, method='Lateralising')
        progress_venn(df_ground_truth, method='Localising')


    # 6. plot progress by study type (CS, SS, ET, Other)
    print("6. Venn diagrams by patient selection priors (study type)")
    df_study_type = progress_study_type(df)
    if plot:
        progress_venn_2(df_study_type, method='Lateralising')
        progress_venn_2(df_study_type, method='Localising')

    print('Other criteria: ',  df.loc[df['Other (e.g. Abs)'].notnull()]['Other (e.g. Abs)'].unique() )
    print('Lateralising Other Total/Exclusives: ', df_study_type.loc['OTHER', ('Lateralising Datapoints', 'Total')], '/',
                                                    df_study_type.loc['OTHER', ('Lateralising Datapoints', 'Exclusive')] )
    print('Localising Other Total/Exclusives: ', df_study_type.loc['OTHER', ('Localising Datapoints', 'Total')], '/',
                                                    df_study_type.loc['OTHER', ('Localising Datapoints', 'Exclusive')] )

    return df, df_ground_truth, df_study_type
