from .QUERY_SEMIOLOGY import QUERY_SEMIOLOGY
import numpy as np
import pandas as pd
from pathlib import Path
import logging

POST_OP = 'Post-op Sz Freedom (Engel Ia, Ib; ILAE 1, 2)'
CONCORDANT = 'Concordant Neurophys & Imaging (MRI, PET, SPECT)'
SEEG_ES = 'sEEG (y) and/or ES (ES)'  # March 2020 version


def exclude_postictals(df):
    """
    Exclude post-ictal semiology.
    This is an individual semiology option.
    """
    df2 = df.copy()
    post_ictals = ['post-ictal', 'postictal', 'post ictal', 'post_ictal']
    post_ictal_inspection, num_query_lat, num_query_loc = QUERY_SEMIOLOGY(df2, semiology_term=post_ictals,
                                                                          ignore_case=True, semiology_dict_path=None,
                                                                          exclude_postictals=True)
    df2.drop(labels=post_ictal_inspection.index,
             axis='index', inplace=True, errors='ignore')
    # logging.debug('Excluded post-ictal semiology in specific query')
    return df2


def exclusions(df,
               POST_ictals=True,
               PET_hypermetabolism=True,
               SPECT_PET=False,
               CONCORDANCE=False,
               ):
    """
    Exclude certain semiologies and criteria prior to performing searches on the df.

    Note PET_hypermetabolism is a subset of SPECT_PET which is itself a subset of CONCORDANCE.
    SPECT_PET also excludes fMRI DTI when no structural MRI lesion.

    """

    if POST_ictals:
        df = exclude_postictals(df)

    if PET_hypermetabolism:
        col1 = CONCORDANT
        pet = ['PET']

        pet_inspection, num_query_lat, num_query_loc = QUERY_SEMIOLOGY(df, semiology_term=pet,
                                                                       ignore_case=True, semiology_dict_path=None,
                                                                       col1=col1, col2=col1,
                                                                       )

        hyper = ['Hyper']
        hyper_inspection, num_query_lat, num_query_loc = QUERY_SEMIOLOGY(df, semiology_term=hyper,
                                                                         ignore_case=True, semiology_dict_path=None,
                                                                         col1=col1, col2=col1,
                                                                         exclude_PET_Hypermetabolism=True)

        # ans is df of the intersection of the above two, keep the index otherwise it is reset
        ans = hyper_inspection.reset_index().merge(
            pet_inspection, how="inner").set_index('index')
        # set them equal to np.nan
        df.loc[list(ans.index), CONCORDANT] = np.nan

        # remember, we don't want to exclude at the outset those who meet other criteria
        # in addition to having PET hypermetabolism as a concordance ground truth:
        ans2 = pd.merge(ans, df.loc[df[POST_OP].isnull()], how='inner')
        ans3 = pd.merge(ans2, df.loc[df[SEEG_ES].isnull()], how='inner')

        df.drop(labels=list(ans3.index), axis='index', inplace=True,
                errors='ignore')  # drops from df altogether

        # # find the indices where concordance was PET hypermetabolism but other criteria were notnull
        # mixed_ground_truth_index = [item for item in list(ans.index) if item not in list(ans3.index)]
        # df.loc[mixed_ground_truth_index][CONCORDANT] =  np.nan # doesn't drop, as meet other ground truth criteria. Just turn concordance to null.

        logging.debug(
            'Excluded cases if PET hypermetabolism was the only grund truth, converted rest to nulls')

    if SPECT_PET:
        col1 = 'Concordant Neurophys & Imaging (MRI, PET, SPECT)'
        col2 = col1
        spect_pet = ['SPECT', 'PET', 'FDG-PET', 'SPECT scan', 'PET scan', 'ictal SPECT', 'interictal PET', 'inter-ictal PET',
                     'PET+ictal SPECT', 'Surgical finding, PET hypometabolism', 'fMRI+DTI', 'PET (interictal hypometabolism)']
        spect_pet_inspection, num_query_lat, num_query_loc = QUERY_SEMIOLOGY(df, semiology_term=spect_pet,
                                                                             ignore_case=True, semiology_dict_path=None,
                                                                             col1=col1, col2=col2,
                                                                             exclude_SPECT_PET=True)

        # SPECT or PET and no other ground truth criteria:
        ans = spect_pet_inspection.reset_index().merge(
            df.loc[df[POST_OP].isnull()], how='inner').set_index('index')

        # change to nans:
        # mixed_ground_truth_index = [item for item in list(spect_pet_inspection.index) if item not in list(ans2.index)]
        # doesn't drop, as meet other ground truth criteria.
        df.loc[list(ans.index), CONCORDANT] = np.nan

        # drops pure spect/pet cases
        ans2 = ans.reset_index().merge(
            df.loc[df[SEEG_ES].isnull()], how='inner').set_index('index')
        df.drop(labels=list(ans2.index), axis='index',
                inplace=True, errors='ignore')
        logging.debug(
            'Excluded cases where concordance involved SPECT or PET without MRI or other ground truths,')
        logging.debug('converted rest to nulls')

    df = df.dropna(axis='columns', how='all')

    # concordance after dropping columns, otherwise would drop this column
    if CONCORDANCE:
        df.loc[:, CONCORDANT] = np.nan
        logging.debug('\nEntirely replaced concordant column with nans')
        # now need to recheck and drop any rows which have no ground truth:
        df.dropna(subset=[POST_OP, CONCORDANT, SEEG_ES],
                  thresh=1, axis=0, inplace=True)
    return df


def exclude_ET(df):
    """
    Exclude ALL epilepsy topology cases EVEN if there are other selection priors (as part of TS filter).
    e.g. some articles may pre-select patients with TLE then also look at ictal cough.
    This exclusion, removes this data even though it was both ET and SS.
    (on the fly as the data grows, rather than using the pickled resources)
    """
    ET = 'Epilepsy Topology (ET)'
    df_exclusions_ET = df.loc[~df[ET].notnull(), :]
    return df_exclusions_ET


def exclude_spontaneous_semiology(df):
    """
    Exclude cases spontaneous semiology cases if this is the only publication approach.
    """
    SS = 'Spontaneous Semiology (SS)'
    ET = 'Epilepsy Topology (ET)'
    CES = 'Cortical Stimulation (CS)'
    subset = [SS, ET, CES]
    df_exclusions_SS = df.copy()
    mask_SS_True = df_exclusions_SS[SS].notnull()
    df_exclusions_SS.loc[mask_SS_True, SS] = np.nan
    df_exclusions_SS = df_exclusions_SS.dropna(subset=subset, thresh=1, axis=0, inplace=False)
    return df_exclusions_SS


def exclude_cortical_stimulation(df):
    """
    Exclude all cortical electrical stimulation publication approaches (as part of TS filter)
    """
    # df_excl = df.copy()
    # mask_string = df_excl[SEEG_ES].str.contains('ES', case=False, na=False)
    # df_excl.loc[mask_string, SEEG_ES] = np.nan
    # subset = [POST_OP, CONCORDANT, SEEG_ES]
    # df_exclusions_CES = df_excl.dropna(subset=subset, thresh=1, axis=0, inplace=False)
    # return df_exclusions_CES
    # second part for test later
    CES = 'Cortical Stimulation (CS)'
    df_exclusions_CES = df.loc[~df[CES].notnull(), :]
    return df_exclusions_CES


def exclude_sEEG(df):
    """
    Exclude cases where the only ground truth is stereo EEG cases.
    I recommend also excluding exclude_cortical_stimulation if running this.

    NB
        df.loc[df[SEEG_ES] == 'y', SEEG_ES] = np.nan
            looks for exact match.
    Whereas
        df.loc[df[SEEG_ES].str.contains('y', na=False), SEEG_ES] = np.nan
            will match both sEEG (y), and sEEG and cortical stimulation (ES), but not ES on its own.
    """
    df.loc[df[SEEG_ES] == 'y', SEEG_ES] = np.nan
    df_exclusions_sEEG = df.dropna(
        subset=[POST_OP, CONCORDANT, SEEG_ES], thresh=1, axis=0, inplace=False)
    return df_exclusions_sEEG


def exclude_seizure_free(df):
    """
    Exclude seizure-free cases if this is the only ground truth.
    """
    df.loc[df[POST_OP].notnull(), POST_OP] = np.nan
    df_exclusion_sz_free = df.dropna(
        subset=[POST_OP, CONCORDANT, SEEG_ES], thresh=1, axis=0, inplace=False)
    return df_exclusion_sz_free


def exclude_paediatric_cases(df):
    """
    Exclude ALL cases labelled as paediatric, i.e. < 7 years old.
    (If the data is mixed and undifferentiated by < 7 yrs, the data is excluded only if the label 'y' was added during data collection.
    This decision was made based on the number of cases under or above 7. If left blank, cases are included.)
    """
    PAED = 'paediatric subgroup <7 years (0-6 yrs) y/n'
    df_exclusions_paeds = df.loc[~(df[PAED] == 'y'), :]
    return df_exclusions_paeds


def only_paediatric_cases(df):
    """
    Only query paediatric cases under 7 years
    """
    PAED = 'paediatric subgroup <7 years (0-6 yrs) y/n'
    df_only_paeds = df.loc[(df[PAED] == 'y'), :]
    return df_only_paeds


def only_postictal_cases(df):
    """
    Only include postictal semiology.
    This is an individual semiology option to use with any semiology beginning with "postictal" e.g. in the SemioDict YAML file.
    """
    df2 = df.copy()
    post_ictals = ['post-ictal', 'postictal', 'post ictal', 'post_ictal']
    post_ictal_inspection, num_query_lat, num_query_loc = QUERY_SEMIOLOGY(df2, semiology_term=post_ictals,
                                                                          ignore_case=True, semiology_dict_path=None,
                                                                          only_postictals=True)
    only_postictal_cases = df2.loc[post_ictal_inspection.index, :]
    # logging.debug('Included only postictal semiology in query')
    return only_postictal_cases
