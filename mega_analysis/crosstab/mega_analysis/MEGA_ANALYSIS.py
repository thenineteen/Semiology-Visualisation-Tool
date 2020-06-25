import logging

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from .cleaning import cleaning
from .exclusions import exclusions
from .group_columns import (anatomical_regions, full_id_vars,
                            lateralisation_vars)
from .missing_columns import missing_columns
from .progress_stats import progress_stats, progress_venn
from .progress_study_type import progress_study_type, progress_venn_2


def MEGA_ANALYSIS(
    excel_data,
    n_rows=2815,
    usecols="A:DY",
    header=1,
    exclude_data=False,
    plot=True,
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

    method to lookup specific semiology and paper using multiIndex:
        change pd.read_excel below first
        df.loc[df.loc[('Aphasia')].index.str.contains('Afif') ]


    returns:
        df: the entire databse cleaned preprocessed etc as a DataFrame
        df_ground_truth: a DataFrame that splits the datapoints by ground truth
        df_study_type: a DataFrame that splits the datapoints by prior study selection (publication approach)
        num_database_articles: integer of number of studies in the entire database (not queried yet)
        num_database_patients: int of number of total patients in entire database (not queried yet)
        num_database_lat: sum of total number of lateralising patient-semiology datapoints in database
        num_database_loc: sum of total number of localising patient-semiology datapoints in database


    Ali Alim-Marvasti July Aug 2019
    """
    df = pd.read_excel(
        excel_data,
        nrows=n_rows,
        usecols=usecols,
        header=header,
    )

    # 0. CLEANUPS: remove empty rows and columns
    logging.debug('\n\n0. DataFrame pre-processing and cleaning:')
    df = cleaning(df)

    # 1. Exclusions
    if exclude_data:
        logging.debug('\n\n1. Filtering data')
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

        # logging.debug('\ndf.shape after exclusions: {}'.format(df.shape))
    else:
        logging.debug('\n\n1. Data not filtered.')

    # 2. checking for missing labels e.g. Semiology Categories Labels:
    logging.debug('\n\n2. Checking for missing column values')
    missing_columns(df)

    # localisation_labels = run anatomical regions
    localisation_labels = anatomical_regions(df)
    first_ = localisation_labels[0]
    logging.debug(
        f'\n\nChecking dtypes: first localisation_labels column is: {first_}.')
    logging.debug(f'\n...last one is {localisation_labels[-1]}')
    for col in df[localisation_labels]:
        for val in df[col]:
            if (type(val) != (np.float)) & (type(val) != (np.int)):
                logging.debug(f'{type(val)} {col} {val}')

    # 3 ffill References:
    df.Reference.fillna(method='ffill', inplace=True)
    logging.debug('\n\n3. forward filled references')

    # 4 check no other entries besides "ES" and "y" in
    # list(df['sEEG and/or ES'].unique())
    # March 2020 updated sEEG_ES = 'sEEG (y) and/or ES (ES)'
    sEEG_ES = 'sEEG (y) and/or ES (ES)'  # March 2020 version
    logging.debug(
        f'\n\n4. sEEG and/or ES set labels include: {list(df[sEEG_ES].unique())}')

    # 5. Some basic progress stats:
    logging.debug('\n\n 5. BASIC PROGRESS:')
    num_database_articles = int(df["Reference"].nunique())
    num_database_patients = int(df["Tot Pt included"].sum())
    num_database_lat = df.Lateralising.sum()
    num_database_loc = df.Localising.sum()

    df_ground_truth = progress_stats(df)

    # plot progress by ground truth
    if plot:
        progress_venn(df_ground_truth, method='Lateralising')
        progress_venn(df_ground_truth, method='Localising')

    # 6. plot progress by study type (CS, SS, ET, Other)
    if plot:
        logging.debug(
            "\n\n6. Venn diagrams by patient selection priors (study type)")
        df_study_type = progress_study_type(df)
        progress_venn_2(df_study_type, method='Lateralising')
        progress_venn_2(df_study_type, method='Localising')

    other_ = df.loc[df["Other factors (e.g. Abs, genetic mutations)"].notnull(),
                    "Other factors (e.g. Abs, genetic mutations)"].unique()
    lat_other_exc = df_study_type.loc["OTHER",
                                      ("Lateralising Datapoints", "Exclusive")]
    logging.debug(
        f'Other criteria: {other_}')
    logging.debug(
        'Lateralising Other Total/Exclusives: '
        f'{df_study_type.loc["OTHER", ("Lateralising Datapoints","Total")]}'
        '/'
        f'{lat_other_exc}'
    )
    logging.debug(
        'Localising Other Total/Exclusives: '
        f'{df_study_type.loc["OTHER", ("Localising Datapoints","Total")]}'
        '/'
        f'{df_study_type.loc["OTHER", ("Localising Datapoints","Exclusive")]}'
    )

    return (df, df_ground_truth, df_study_type,
            num_database_articles, num_database_patients, num_database_lat, num_database_loc)
