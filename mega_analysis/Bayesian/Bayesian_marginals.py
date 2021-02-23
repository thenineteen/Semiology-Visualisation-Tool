from mega_analysis.crosstab.file_paths import file_paths
from mega_analysis.semiology import Semiology, Laterality
from mega_analysis.crosstab.mega_analysis.MEGA_ANALYSIS import MEGA_ANALYSIS
from mega_analysis.crosstab.mega_analysis.QUERY_SEMIOLOGY import QUERY_SEMIOLOGY
from mega_analysis.crosstab.all_localisations import all_localisations
from mega_analysis.crosstab.mega_analysis.exclusions import (exclude_ET, exclude_cortical_stimulation, exclude_spontaneous_semiology,
                                                             exclude_postictals)
from mega_analysis.crosstab.lobe_top_level_hierarchy_only import top_level_lobes
from mega_analysis.semiology import recursive_items
from mega_analysis.Sankey_Functions import normalise_top_level_localisation_cols

import pandas as pd
import os
import yaml
import copy
os.chdir('C:/Users/ali_m/AnacondaProjects/PhD/Semiology-Visualisation-Tool/')


def query_semiology_wrapper_from_scripts(df, semiology_list, semiology_dict_path):
    """
    From scripts/figures.py in kd_figures-v3 branch
    """
    query_results = {}
    for semiology in semiology_list:
        query_inspection, num_query_lat, num_query_loc = QUERY_SEMIOLOGY(df,
                                                                         semiology_term=semiology,
                                                                         ignore_case=True,
                                                                         semiology_dict_path=semiology_dict_path,
                                                                         all_columns_wanted=True)
        # col1=col1, col2=col1)

        one_query_result = {
            'query_inspection': query_inspection,
            'num_query_lat': num_query_lat,
            'num_query_loc': num_query_loc
        }
        query_results[semiology] = one_query_result
    return query_results


def get_summary_semio_loc_df_from_scripts():
    """
    Lots of copy pasting from scripts/figures.py in kd_figures-v3 branch.

    returns query_results which is a nested dictionary
        full
        spontaneous
        topology
            {semiologies}
                query_inspection
                num_query_loc
                num_query_lat
    """

    # Define paths
    repo_dir, resources_dir, excel_path, semiology_dict_path = file_paths()

    Semio2Brain_Database = excel_path
    with open(semiology_dict_path) as f:
        SemioDict = yaml.load(f, Loader=yaml.FullLoader)

    region_names = all_localisations()
    semiology_list = list(recursive_items(SemioDict))

    (original_df,
     df_ground_truth, df_study_type,
     num_database_articles, num_database_patients, num_database_lat, num_database_loc) = \
        MEGA_ANALYSIS(Semio2Brain_Database,
                      exclude_data=True)

    # -----------------------------------
    redistribution_spec = {
        'FT': ['FL', 'INSULA', 'Lateral Temporal', 'TL'],
        'TO': ['Lateral Temporal', 'TL', 'OL'],
        'TP': ['Lateral Temporal', 'TL', 'PL'],
        'FTP': ['INSULA', 'Lateral Temporal', 'TL', 'FL', 'PL'],
        'TPO Junction': ['Lateral Temporal', 'TL', 'PL', 'OL'],
        'PO': ['PL', 'OL'],
        'FP': ['FL', 'PL'],
        'Perisylvian': ['INSULA', 'Lateral Temporal', 'TL', 'FL', 'PL'],
        'Sub-Callosal Cortex': ['Ant Cing (frontal, genu)', 'CING']
    }
    redistributed_df = copy.deepcopy(original_df)
    # probably not needed as used exclude_data True when calling M_A
    redistributed_df = exclude_postictals(redistributed_df)

    for from_region, destination_regions in redistribution_spec.items():
        for destination in destination_regions:
            redistributed_df[destination] = original_df[destination].fillna(
                0) + original_df[from_region].fillna(0)
    redistributed_df = redistributed_df.drop(redistribution_spec.keys(), 'columns')
    # -----------------------------------

    # region_names_re = region_names
    # region_names_re['top_level'] = ['TL',
    #                                 'FL',
    #                                 'CING',
    #                                 'PL',
    #                                 'OL',
    #                                 'INSULA',
    #                                 'Hypothalamus',
    #                                 'Cerebellum', ]
    # region_names_re['top_level_all_other'] = ['Cerebellum']

    df = copy.deepcopy(redistributed_df)
    df_SS = exclude_ET(df)
    df_SS = exclude_cortical_stimulation(df_SS)
    df_TS = exclude_spontaneous_semiology(df)

    all_dfs = {
        'full': df,
        'spontaneous': df_SS,
        'topology':  df_TS,
    }

    query_results = {}
    for key, df in all_dfs.items():
        query_results[key] = query_semiology_wrapper_from_scripts(df, semiology_list, semiology_dict_path)

    return query_results


def marginal_GIF_probabilities(all_combined_gifs):
    """
    Input the DataFrame of GIF Parcellations and values for all semiologies.
        all_combined_gifs: GIF values
            all_combined_gifs is a heatmap df i.e. from patient.get_num_datapoints_dict()  # for all data not for single semiology
            remember the cols of all_combined_gifs are "Gif Parcellations" and "pt #s"

    Returns the marginal_probabilities.

    Future: As sensitivity analyses, should check the variance of marginal prob when using different filters
        concretely: marginal_p should be using all the data without filters, but then when using filters, see if we
        had used a filtered df using one of the exclusions (e.g. EZ only or based on age),
        how much would the marginal_p differ and Bayesian inference vary by?

    Alim-Marvasti Feb 2021
    """

    # Localisations
    gif_df = all_combined_gifs.copy()
    gif_df = gif_df.fillna(0)
    gif_df['pt #s'] = gif_df['pt #s'] / (gif_df['pt #s'].sum())
    marginal_GIF_prob = gif_df

    return marginal_GIF_prob


def marginal_Localisation_and_Semiology_probabilities(df=None,
                                                    normalised=True,
                                                    publication_prior='full'):
    """ Returns the marginal localisation and semiology probabilities

    > df (optional): preprocessed Semio2Brain DataFrame obtained from MEGA_ANALYSIS after hierarchy reversal.
        df = MEGA_ANALYSIS()  # for all-data
        also used SemioDict
        df = hierarchy_reversal()
            Assume df is the fully cleaned and hierarchy reversed Semio2Brain descriptions
            (or if not hierarchy reveresed, then top-level regions only)

        I.e. Use get_summary_semio_loc_df_from_scripts() to get df of semiology by localisation
            as uses top-level regions only without hierarchy_reversal.
            rows: semiologies
            columns: localisations
            can be normalised or not normalised

    > publication_prior: 'full', 'spontaneous', or 'topological'

    returns:
        marginal_semio_prob: DataFrame with index of semiologies, and single column of marginal 'probability' (col df)
        marginal_loc_prob: df with columns as localisations (row df)
    """
    # useful for both semio and unnormalised locs:
    Lobes = top_level_lobes(Bayesian=True)

    # make the df in the form of semiology/locs
    marginal_semio_df = pd.DataFrame()
    query_results = get_summary_semio_loc_df_from_scripts()
    if normalised:
        for semio, v in query_results[publication_prior].items():
            marginal_semio_df.loc[semio, 'num_query_loc'] = query_results[publication_prior][semio]['num_query_loc']
    elif not normalised:
        for semio, v in query_results[publication_prior].items():
            semio_top_level_sum = query_results[publication_prior][semio]['query_inspection'][Lobes].sum()
            marginal_semio_df.loc[semio, 'not_norm'] = semio_top_level_sum.sum()
    # for each semiology, divide by the total, to get the marginal probability of that semiology i.e.
    marginal_semio_prob = marginal_semio_df / marginal_semio_df.sum()
    marginal_semio_prob.rename(columns={'num_query_loc':'probability',
                                        'not_norm':'probability'},
                                        inplace=True, errors='ignore')

    # do the same for the localisations:
    temp_df = pd.DataFrame()
    marginal_loc_df = pd.DataFrame()
    for semio, v in query_results[publication_prior].items():
        temp_df = query_results[publication_prior][semio]['query_inspection'][Lobes]
        if normalised:
            temp_df = normalise_top_level_localisation_cols(temp_df)
        marginal_loc_df = (marginal_loc_df.add(temp_df, fill_value=0))

    marginal_loc_df.fillna(0, inplace=True)
    marginal_loc_prob = marginal_loc_df.sum(axis=0) / marginal_loc_df.sum().sum()

    return marginal_semio_prob, marginal_loc_prob


def p_GIFs(global_lateralisation=False,
           include_paeds_and_adults=True,
           include_only_postictals=False,
           symptom_laterality='neutral',
           dominance='neutral',
           ):
    """
    Return the normalised/unnormalised marginal probabilities for each GIF parcellation.
        for ictal semiologies only (excluding postictals)

    see marginal_GIF_probabilities() for sensitivity analyses
        e.g. by adding include_concordance=False for data queries excluding concordance
            or changing laterality or age
    """

    # normalised
    patient_all_semiology_norm = Semiology(
                                            ".*",
                                            symptoms_side=Laterality.NEUTRAL,
                                            dominant_hemisphere=Laterality.NEUTRAL,
                                            include_postictals=False,
                                            include_paeds_and_adults=include_paeds_and_adults,
                                            normalise_to_localising_values=True,
                                            global_lateralisation=global_lateralisation,
                                        )

    if symptom_laterality == 'left':
        patient_all_semiology_norm.symptoms_side = Laterality.LEFT
    if dominance == 'left':
        patient_all_semiology_norm.dominant_hemisphere = Laterality.LEFT

    patient_all_semiology_norm.include_only_postictals = include_only_postictals
    all_combined_gifs_norm = patient_all_semiology_norm.get_num_datapoints_dict()
    p_GIF_norm = marginal_GIF_probabilities(all_combined_gifs_norm)

    # now not normalised version
    patient_all_semiology_notnorm = Semiology(
                                                ".*",
                                                symptoms_side=Laterality.symptom_laterality,
                                                dominant_hemisphere=Laterality.dominance,
                                                include_postictals=False,
                                                include_paeds_and_adults=include_paeds_and_adults=True,
                                                normalise_to_localising_values=False,
                                                global_lateralisation=global_lateralisation,
                                            )
    patient_all_semiology_notnorm.include_only_postictals = include_only_postictals
    all_combined_gifs_notnorm = patient_all_semiology_notnorm.get_num_datapoints_dict()
    p_GIF_notnorm = marginal_GIF_probabilities(all_combined_gifs_notnorm)

    return p_GIF_norm, p_GIF_notnorm


def p_Semiology(publication_prior='full'):
    """
    Return the normalised and unnormalised marginal probabilities for ictal semiologies.
    """
    p_S_norm, p_Loc_norm = marginal_Localisation_and_Semiology_probabilities(normalised=True, publication_prior=publication_prior)
    p_S_notnorm, p_Loc_notnorm = marginal_Localisation_and_Semiology_probabilities(normalised=False, publication_prior=publication_prior)

    return p_S_norm, p_Loc_norm, p_S_notnorm, p_Loc_notnorm
