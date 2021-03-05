import logging
import pandas as pd
import numpy as np

from .mapping import big_map, pivot_result_to_one_map
from .group_columns import full_id_vars, lateralisation_vars
from .melt_then_pivot_query import melt_then_pivot_query


# main function is QUERY_LATERALISATION


def gifs_lat(gif_lat_file):
    """
    factor function. opens the right/left gif parcellations from excel and extracts the right/left gifs as series/list.
    """
    gifs_right = gif_lat_file.loc[gif_lat_file['R'].notnull(), 'R'].copy()
    gifs_left = gif_lat_file.loc[gif_lat_file['L'].notnull(), 'L'].copy()

    return gifs_right, gifs_left


def summarise_overall_lat_values(df_or_row,
                                 side_of_symptoms_signs,
                                 pts_dominant_hemisphere_R_or_L,
                                 Right=0,
                                 Left=0,
                                 **kwargs,
                                 ):
    """
    Factor function for Q_L. Calculated IL, CL, DomH and NonDomH lateralisations.
    """
    if 'IL' not in kwargs:
        IL = df_or_row['IL'].sum()
        CL = df_or_row['CL'].sum()
        DomH = df_or_row['DomH'].sum()
        NonDomH = df_or_row['NonDomH'].sum()
        # BL =df_or['BL (Non-lateralising)'].sum()
    else:
        IL = kwargs['IL']
        CL = kwargs['CL']
        DomH = kwargs['DomH']
        NonDomH = kwargs['NonDomH']

    # pt input
    if side_of_symptoms_signs == 'R':
        Right += IL
        Left += CL

    elif side_of_symptoms_signs == 'L':
        Right += CL
        Left += IL

    if pts_dominant_hemisphere_R_or_L:
        if pts_dominant_hemisphere_R_or_L == 'R':
            Right += DomH
            Left += NonDomH
        elif pts_dominant_hemisphere_R_or_L == 'L':
            Right += NonDomH
            Left += DomH
    return Right, Left


def QUERY_LATERALISATION_GLOBAL(semiology_term, inspect_result, df, one_map, gif_lat_file,
                                side_of_symptoms_signs=None,
                                pts_dominant_hemisphere_R_or_L=None,
                                normalise_lat_to_loc=False):
    """
    After obtaining inspect_result and clinician's filter, can  use this function to determine
    lateralisation.

    Run this after QUERY_SEMIOLOGY OR QUERY_INTERSECTION_TERMS

    inspect_result may not have a lateralising column (if all were NaNs)
    Whereas QUERY_LATERALISATION goes through row by row, this is global.

    ---
    > inspect_result is obtained from QUERY_SEMIOLOGY OR QUERY_INTERSECTION_TERMS
    > df as per pivot_result_to_pixel_intensities's df
    > side_of_symptoms_signs: 'R' or 'L' - side of symptoms/signs on limbs
    > pts_dominant_hemisphere_R_or_L: if known from e.g. fMRI language 'R' or 'L'
    >> gifs_not_lat is the same as localising_only
    >> lat_only_Right/Left lateralising only data

    returns:
        all_combined_gifs: similar in structure to output of pivot_result_to_one_map (final step),
                        # s rather than pixel intensity.
                        but in this case, the output column is pt
        num_QL_lat: Lateralising Datapoints relevant to query {semiology_term}.
                    Should be exactly the same as num_query_lat returned by QUERY_SEMIOLOGY.
        num_QL_CL: Datapoints that lateralise contralateral to the semiology query {semiology_term}
        num_QL_IL: Datapoints that lateralise ipsilaterally to the semiology query {semiology_term}
        num_QL_BL: Study reports the datapoint as being Bilateral. Non-informative and not utilised.
        num_QL_DomH: Semiology datapoints lateralising to the Dominant Hemisphere
        num_QL_NonDomH: Semiology datapoints lateralising to Non-Dominant Hemisphere

    ---
    NB theoretically supports normalise_lat_to_loc but hasn't been tested

    Alim-Marvasti Feb 2021
    """
    pd.options.mode.chained_assignment = 'raise'
    df = df.copy()
    logging.debug(f'\n\n Global Lateralisation enabled.')

    # -------------LOTS OF CHECKS-------------
    # ensure there is patient's lateralised signs and check dominant known or not
    if not side_of_symptoms_signs and not pts_dominant_hemisphere_R_or_L:
        # print('Please note you must determine at least one of side_of_symptoms_signs or')
        # print('pts_dominant_hemisphere_R_or_L keyword arguments for lateralised data extraction.')
        no_lateralising_data = True

    # check there is lateralising value
    try:
        num_QL_lat = inspect_result['Lateralising'].sum()
        if num_QL_lat > 0:
            no_lateralising_data = False
            logging.debug(f'\n\nLateralisation based on: {num_QL_lat.sum()} datapoints')
        else:
            # no lateralising data
            no_lateralising_data = True
            # num_QL_lat = None
            # return None, None, None, None, None, None, None
    except KeyError:
        # logging.debug(f'No Lateralising values found for this query of the database.')
        no_lateralising_data = True
        # num_QL_lat = None
        # return None, None, None, None, None, None, None

    lat_vars = [i for i in lateralisation_vars() if i not in ['Lateralising']]

    # check that the lateralising columns isn't null where it shouldn't be i.e. CL/IL/DomH/NonDomH not null:
    # but not 'BL (Non-lateralising)'
    # first ensure other columns all feature in this inspect_result:
    inspect_result2 = inspect_result.copy()
    for col in lat_vars:
        if col not in inspect_result2.columns:
            inspect_result2[col] = np.nan
    # now can check lateralising columns isn't null where it shouldn't be:
    missing_lat = inspect_result2.loc[(inspect_result2['CL'].notnull()) |
                                      (inspect_result2['IL'].notnull()) |
                                      (inspect_result2['DomH'].notnull()) |
                                      (inspect_result2['NonDomH'].notnull()), :].copy()
    missing_lat_null_mask = missing_lat['Lateralising'].isnull()
    if not missing_lat_null_mask.all():
        # logging.debug('\nNo missing Lateralising data points.')
        pass
    else:
        logging.debug(
            'The inspect_result lat col has NaNs/zero where it should not: autofilled')
        df_of_missing_lats = missing_lat.loc[missing_lat_null_mask].copy()
        df.loc[df_of_missing_lats.index, 'Lateralising'] = df_of_missing_lats[[
            'CL', 'IL', 'DomH', 'NonDomH']].sum(axis=1)

    # check columns exist (not removed in preceding notnull steps from other functions):
    for col in lat_vars:
        if col not in inspect_result.columns:
            inspect_result[col] = 0
    # -------------CHECKS END-------------

    # summarise lat values
    IL = inspect_result['IL']
    CL = inspect_result['CL']
    DomH = inspect_result['DomH']
    NonDomH = inspect_result['NonDomH']
    BL = inspect_result['BL (Non-lateralising)']
    num_QL_CL = CL.sum()
    num_QL_IL = IL.sum()
    num_QL_BL = BL.sum()
    num_QL_DomH = DomH.sum()
    num_QL_NonDomH = NonDomH.sum()
    total_QL_lat = num_QL_CL+num_QL_IL+num_QL_DomH+num_QL_NonDomH
    logging.debug(f'\n\nOverall Contralateral: {num_QL_CL} datapoints')
    logging.debug(f'Ipsilateral: {num_QL_IL} datapoints')
    logging.debug(f'Bilateral/Non-lateralising: {num_QL_BL} datapoints. This is not utilised.')
    logging.debug(f'Dominant Hemisphere: {num_QL_DomH} datapoints')
    logging.debug(f'Non-Dominant Hemisphere: {num_QL_NonDomH} datapoints')
    logging.debug(f'lateralising col sum: {num_QL_lat}. total_QL_lat: {total_QL_lat}.')

    # Global initialisation:
    gifs_right, gifs_left = gifs_lat(gif_lat_file)

    # map localisations to gif parcellations all in one go (not by row)
    pivot_result = melt_then_pivot_query(df, inspect_result, semiology_term)
    all_combined_gifs = pivot_result_to_one_map(pivot_result, one_map)

    # convert to binary R vs L values
    Right, Left = \
        summarise_overall_lat_values(inspect_result, side_of_symptoms_signs, pts_dominant_hemisphere_R_or_L)
    Total = Right+Left
    if Total == 0:
        no_lateralising_data = True  # in case Localising col >0 but this still zero
    if Right == Left:
        Right_equal_Left = True
    elif Right != Left:
        Right_equal_Left = False


    # remove NaNs to allow div by 2 and multiplication by RR_norm:
    all_combined_gifs.fillna(value=0, inplace=True)

    # -------------Scenario 1: No lateralising data or equal R and L---------------
    # the localising values should be split equally in half between the right and left GIFs
    # this is different to the default behaviour of the original QUERY_LATERALISTION, but more intuitive
    if no_lateralising_data or Right_equal_Left:
        all_combined_gifs['pt #s'] = all_combined_gifs['pt #s']/2
    # -------------END---------------------------------------------------------


    # If lateralising data, find lowest value of R or L, proprotions and RR and RR_norm:
    elif not no_lateralising_data and not Right_equal_Left:
        lower_postn = np.argmin([Right, Left])
        if lower_postn == 0:
            isin_lower = gifs_right  # reduce right sided intensities/pt #s
            isin_higher = gifs_left
        elif lower_postn == 1:
            isin_lower = gifs_left
            isin_higher = gifs_right

        lower_value = [Right, Left][lower_postn]
        higher_value = [Right, Left]
        higher_value.remove(lower_value)
        RR = lower_value / Total
        OR = lower_value / higher_value

        # now should be able to use above to lateralise the localising gif parcellations:
        # if there are 100 localisations in one row, and only 1 IL And 3 CL, it would be too much
        # to say the IL side gets one third of the CL side as number of lat is too low
        # hence normalise by dividing by proportion_lateralising (which is between (0,1])

        # set the scale of influence of lateralisation on the gif parcellations
        # in case there are missing laterlisations vs CL/IL/Dom/NonDom numbers, use total_QL_lat:
        proportion_lateralising = total_QL_lat / inspect_result['Localising'].sum()

        if normalise_lat_to_loc == True:
            # see comments on section above about why we should normalise
            RR_norm = RR * proportion_lateralising
            if RR_norm > 1:
                RR_norm = 1
                logging.debug('normalised RR capped at 1: lateralising > localising data')
        elif normalise_lat_to_loc == False:
            # default counter argument: clinically we treat lat and loc entirely separately
            RR_norm = RR

        # -------------Scenario 2: Unequal lateralising data: RR_norm and 1-RR_norm---------------
        df_lower_lat_to_be_reduced = all_combined_gifs.loc[all_combined_gifs['Gif Parcellations'].isin(list(isin_lower))].copy()
        # now make these values lower by a proportion = RR_norm (in this case RR_norm = RR as denom is 1)
        reduce_these = df_lower_lat_to_be_reduced.loc[:, 'pt #s'].copy()
        df_lower_lat_to_be_reduced.loc[:, 'pt #s'] = RR_norm * reduce_these
        # re attribute these corrected reduced lateralised values to the entire row's data:
        all_combined_gifs.loc[df_lower_lat_to_be_reduced.index, :] = df_lower_lat_to_be_reduced

        # now repeat the above steps for the higher values i.e. contralateral side
        df_higher_lat_to_be_reduced = all_combined_gifs.loc[all_combined_gifs['Gif Parcellations'].isin(list(isin_higher))].copy()
        reduce_these = df_higher_lat_to_be_reduced.loc[:, 'pt #s'].copy()
        df_higher_lat_to_be_reduced.loc[:, 'pt #s'] = (1-RR_norm) * reduce_these
        all_combined_gifs.loc[df_higher_lat_to_be_reduced.index, :] = df_higher_lat_to_be_reduced

        # -------------END----------------------------------------------


    # pivot_table the values
    fixed = all_combined_gifs.pivot_table(
        columns='Gif Parcellations', values='pt #s', aggfunc='sum')
    fixed2 = fixed.melt(value_name='pt #s')
    fixed2.insert(0, 'Semiology Term', np.nan)
    all_combined_gifs = fixed2
    all_combined_gifs

    return (all_combined_gifs,
            num_QL_lat, num_QL_CL, num_QL_IL, num_QL_BL, num_QL_DomH, num_QL_NonDomH)


def QUERY_LAT_GLOBAL_BAYESIANPOSTERIOR(all_combined_gifs,
                                num_QL_lat, num_QL_CL, num_QL_IL, num_QL_BL, num_QL_DomH, num_QL_NonDomH,
                                gif_lat_file,
                                side_of_symptoms_signs=None,
                                pts_dominant_hemisphere_R_or_L=None,
                                normalise_lat_to_loc=False):
    """
    After obtaining the symmetric posterior-TS only estimate, this function applies global lateralisation.
    This has to be done separately as the posterior-from-TS uses cached data, then we can't run QUERY_LATERALISATION_GLOBAL separately
        because it won't be able to use the bayes rule from cached results.
        i.e., the source of all_combined_gifs argument and the num_QL_lat etc are separate.

    This is just an adapted version of QUERY_LATERALISATION_GLOBAL.

    > all_combined_gifs as pd.DataFrame THIS IS ALTERED IN PLACE AND CHANGES PROPAGATE

    returns as QUERY_LATERALISATION_GLOBAL but probailities not pt #s despite the misnomer in the col names below
    ---
    NB should factorise both functions in future.
    Alim-Marvasti March 2021
    """
    logging.debug(f'\n\n Bayesian Global Lateralisation enabled.')

    # beacuse all_combined_gifs argument comes from Psoteroir_only_cachche.py df_to_dict_like_allcombinedgifs()
    # whereas the previous versions of Q_L calculated it using pivot_result_to_one_map()
        # so need to make cols the same
    if 'pt #s' not in all_combined_gifs.columns:
        all_combined_gifs.rename(columns={0 : 'pt #s'}, inplace=True)

    # -------------A FEW CHECKS-------------
    # ensure there is patient's lateralised signs and check dominant known or not
    if not side_of_symptoms_signs and not pts_dominant_hemisphere_R_or_L:
        no_lateralising_data = True
    # check there is lateralising value
    if num_QL_lat > 0:
        no_lateralising_data = False
        logging.debug(f'\n\n(Bayesian) Global Lateralising data: {num_QL_lat.sum()} datapoints')
    else:
        # no lateralising data
        no_lateralising_data = True


    # summarise lat values
    total_QL_lat = num_QL_CL + num_QL_IL + num_QL_DomH + num_QL_NonDomH
    logging.debug(f'\n\nBayesian values carried over: \nOverall Contralateral= {num_QL_CL} datapoints')
    logging.debug(f'Ipsilateral: {num_QL_IL} datapoints')
    logging.debug(f'Bilateral/Non-lateralising: {num_QL_BL} datapoints. This is not utilised.')
    logging.debug(f'Dominant Hemisphere: {num_QL_DomH} datapoints')
    logging.debug(f'Non-Dominant Hemisphere: {num_QL_NonDomH} datapoints')
    logging.debug(f'lateralising col sum: {num_QL_lat}. total_QL_lat: {total_QL_lat}.')

    # Global initialisation:
    gifs_right, gifs_left = gifs_lat(gif_lat_file)

    # convert to binary R vs L values
    Right, Left = \
        summarise_overall_lat_values(all_combined_gifs,
                                side_of_symptoms_signs,
                                pts_dominant_hemisphere_R_or_L,
                                IL=num_QL_IL,
                                 CL=num_QL_CL,
                                 DomH=num_QL_DomH,
                                 NonDomH=num_QL_NonDomH,
        )
    Total = Right+Left
    if Total == 0:
        no_lateralising_data = True
    if Right == Left:
        Right_equal_Left = True
    elif Right != Left:
        Right_equal_Left = False

    # remove NaNs to allow div by 2 and multiplication by RR_norm:
    all_combined_gifs.fillna(value=0, inplace=True)

    # -------------Scenario 1: No lateralising data or equal R and L---------------
    # the localising values should be split equally in half between the right and left GIFs
    # this is different to the default behaviour of the original QUERY_LATERALISTION, but more intuitive
    if no_lateralising_data or Right_equal_Left:
        logging.debug('\n\nMEGA Q_L_G_B: no_lateralising_data or Right_equal_Left')
        all_combined_gifs['pt #s'] = all_combined_gifs['pt #s']/2
    # -------------END---------------------------------------------------------

    # If lateralising data, find lowest value of R or L, proprotions and RR and RR_norm:
    elif not no_lateralising_data and not Right_equal_Left:
        lower_postn = np.argmin([Right, Left])
        if lower_postn == 0:
            isin_lower = gifs_right  # reduce right sided intensities/pt #s
            isin_higher = gifs_left
        elif lower_postn == 1:
            isin_lower = gifs_left
            isin_higher = gifs_right

        lower_value = [Right, Left][lower_postn]
        higher_value = [Right, Left]
        higher_value.remove(lower_value)
        RR = lower_value / Total
        OR = lower_value / higher_value

        # now should be able to use above to lateralise the localising gif parcellations:
        # if there are 100 localisations in one row, and only 1 IL And 3 CL, it would be too much
        # to say the IL side gets one third of the CL side as number of lat is too low
        # hence normalise by dividing by proportion_lateralising (which is between (0,1])
        # # set the scale of influence of lateralisation on the gif parcellations
        # # in case there are missing laterlisations vs CL/IL/Dom/NonDom numbers, use total_QL_lat:
        # # this normalising lat to loc isn't yet used and if required for Bayesian posterior, need to ensure we pass it in as a value num_QL_LOC

        if normalise_lat_to_loc == True:
            # see comments on section above about why we should normalise
            raise Exception("normalising lateralisation to localisation isn't yet supported")
            proportion_lateralising = total_QL_lat / num_QL_LOC
            RR_norm = RR * proportion_lateralising
            if RR_norm > 1:
                RR_norm = 1
                logging.debug('normalised RR capped at 1: lateralising > localising data')
        elif normalise_lat_to_loc == False:
            # default counter argument: clinically we treat lat and loc entirely separately
            RR_norm = RR
            logging.debug(f'\n\nMEGA Q_LAT_GLOBAL\n\tRR_norm - \t{RR_norm}')

        # -------------Scenario 2: Unequal lateralising data: RR_norm and 1-RR_norm---------------
        df_lower_lat_to_be_reduced = all_combined_gifs.loc[all_combined_gifs.index.isin(list(isin_lower))].copy()
        # now make these values lower by a proportion = RR_norm (in this case RR_norm = RR as denom is 1)
        reduce_these = df_lower_lat_to_be_reduced.loc[:, 'pt #s'].copy()
        df_lower_lat_to_be_reduced.loc[:, 'pt #s'] = RR_norm * reduce_these
        # re attribute these corrected reduced lateralised values to the entire row's data:
        all_combined_gifs.loc[df_lower_lat_to_be_reduced.index, :] = df_lower_lat_to_be_reduced

        # now repeat the above steps for the higher values i.e. contralateral side
        df_higher_lat_to_be_reduced = all_combined_gifs.loc[all_combined_gifs.index.isin(list(isin_higher))].copy()
        reduce_these = df_higher_lat_to_be_reduced.loc[:, 'pt #s'].copy()
        df_higher_lat_to_be_reduced.loc[:, 'pt #s'] = (1-RR_norm) * reduce_these
        all_combined_gifs.loc[df_higher_lat_to_be_reduced.index, :] = df_higher_lat_to_be_reduced

        # -------------END----------------------------------------------

    # # pivot_table the values
    # fixed = all_combined_gifs.pivot_table(
    #     columns='Gif Parcellations', values='pt #s', aggfunc='sum')
    # fixed2 = fixed.melt(value_name='pt #s')
    # fixed2.insert(0, 'Semiology Term', np.nan)
    # all_combined_gifs = fixed2

    logging.debug(f'\n\n!!Bayesian Global lat returns: all_combined_gifs = {all_combined_gifs}')
    return all_combined_gifs