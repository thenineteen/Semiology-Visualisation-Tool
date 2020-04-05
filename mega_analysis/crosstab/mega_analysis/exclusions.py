from .QUERY_SEMIOLOGY import *
import numpy as np
import pandas as pd
from pathlib import Path

post_op = 'Post-op Sz Freedom (Engel Ia, Ib; ILAE 1, 2)'
concordant = 'Concordant Neurophys & Imaging (MRI, PET, SPECT)'
# sEEG_ES = 'sEEG and/or ES'
sEEG_ES = 'sEEG (y) and/or ES (ES)'  # March 2020 version

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
        post_ictals = ['post-ictal', 'postictal', 'post ictal', 'post_ictal']
        post_ictal_inspection = QUERY_SEMIOLOGY(df, semiology_term=post_ictals,
                                                ignore_case=True, semiology_dict_path=None)
        df.drop(labels = post_ictal_inspection.index, axis='index', inplace=True, errors='ignore')
        print('Excluded post-ictal semiology in the query')

    if PET_hypermetabolism:
        col1 = concordant
        pet = ['PET']

        pet_inspection = QUERY_SEMIOLOGY(df, semiology_term=pet,
                                                ignore_case=True, semiology_dict_path=None,
                                                col1=col1, col2=col1)

        hyper = ['Hyper']
        hyper_inspection = QUERY_SEMIOLOGY(df, semiology_term=hyper,
                                                ignore_case=True, semiology_dict_path=None,
                                                col1=col1, col2=col1)

        # ans is df of the intersection of the above two, keep the index otherwise it is reset
        ans = hyper_inspection.reset_index().merge(pet_inspection, how="inner").set_index('index')
        # set them equal to np.nan
        df.loc[list(ans.index), concordant] =  np.nan

        #remember, we don't want to exclude at the outset those who meet other criteria
        #in addition to having PET hypermetabolism as a concordance ground truth:
        ans2 = pd.merge(ans, df.loc[df[post_op].isnull()], how='inner')
        ans3 = pd.merge(ans2, df.loc[df[sEEG_ES].isnull()], how='inner')

        df.drop(labels = list(ans3.index), axis='index', inplace=True, errors='ignore')  # drops from df altogether



        # # find the indices where concordance was PET hypermetabolism but other criteria were notnull
        # mixed_ground_truth_index = [item for item in list(ans.index) if item not in list(ans3.index)]
        # df.loc[mixed_ground_truth_index][concordant] =  np.nan # doesn't drop, as meet other ground truth criteria. Just turn concordance to null.

        print('Excluded cases where PET hypermetabolism was the only grund truth criteria from the query, converted rest to nulls')


    if SPECT_PET:
        col1 = 'Concordant Neurophys & Imaging (MRI, PET, SPECT)'
        col2 = col1
        spect_pet = ['SPECT', 'PET', 'FDG-PET', 'SPECT scan', 'PET scan', 'ictal SPECT', 'interictal PET', 'inter-ictal PET',
                     'PET+ictal SPECT', 'Surgical finding, PET hypometabolism', 'fMRI+DTI', 'PET (interictal hypometabolism)']
        spect_pet_inspection = QUERY_SEMIOLOGY(df, semiology_term=spect_pet,
                                                ignore_case=True, semiology_dict_path=None,
                                                col1=col1, col2=col2)

        # SPECT or PET and no other ground truth criteria:
        ans = spect_pet_inspection.reset_index().merge(df.loc[df[post_op].isnull()], how='inner').set_index('index')

        # change to nans:
        # mixed_ground_truth_index = [item for item in list(spect_pet_inspection.index) if item not in list(ans2.index)]
        df.loc[list(ans.index), concordant] =  np.nan # doesn't drop, as meet other ground truth criteria.

        #drops pure spect/pet cases
        ans2 = ans.reset_index().merge(df.loc[df[sEEG_ES].isnull()], how='inner').set_index('index')
        df.drop(labels = list(ans2.index), axis='index', inplace=True, errors='ignore')
        print('Excluded cases where concordance involved SPECT or PET without MRI or other ground truths,')
        print('converted rest to nulls')

    df = df.dropna(axis='columns', how='all')

    # concordance after dropping columns, otherwise would drop this column
    if CONCORDANCE:
        df.loc[:, concordant] = np.nan
        print('\nEntirely replaced concordant column with nans')
        # now need to recheck and drop any rows which have no ground truth:
        df.dropna(subset=[post_op, concordant, sEEG_ES], thresh=1, axis=0, inplace=True)
    return df


def exclude_ET(df):
    """
    exclude ALL epilepsy topology cases on the fly as the data grows, rather than using the pickled resources
    """
    ET = 'Epilepsy Topology (ET)'
    df_exclusions_ET = df.loc[~df[ET].notnull(), :]
    return df_exclusions_ET


def exclude_cortical_stimulation(df):
    """
    exclude electrical stimulation cases when this is the only ground truth.
    will need a datatest to ensure all sEEG_ES = 'ES' have CES.notnull(). 
    """
    df.loc[df[sEEG_ES]=='ES', sEEG_ES] = np.nan
    df_exclusions_CES = df.dropna(subset=[post_op, concordant, sEEG_ES], thresh=1, axis=0, inplace=False)
    return df_exclusions_CES
    # # second part for test later
    # CES = 'Cortical Stimulation (CS)'
    # df_exclusions_CES = df_exclusions_CES.loc[~df[CES].notnull(), :]
    # return df_exclusions_CES

def exclude_sEEG(df):
    """
    exclude cases where the only ground truth is stereo EEG cases.
    I recommend also excluding exclude_cortical_stimulation if running this.
    """
    df.loc[df[sEEG_ES]=='y', sEEG_ES] = np.nan
    df_exclusions_sEEG = df.dropna(subset=[post_op, concordant, sEEG_ES], thresh=1, axis=0, inplace=False)
    return df_exclusions_sEEG

def exclude_seizure_free(df):
    """
    exclude seizure-free cases if this is the only ground truth.
    """
    df.loc[df[post_op].notnull(), post_op] = np.nan
    df_exclusion_sz_free = df.dropna(subset=[post_op, concordant, sEEG_ES], thresh=1, axis=0, inplace=False)
    return df_exclusion_sz_free

