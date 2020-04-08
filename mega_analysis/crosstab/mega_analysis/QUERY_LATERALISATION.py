import logging
import pandas as pd
import numpy as np
from .mapping import mapping, big_map, pivot_result_to_one_map
from .group_columns import full_id_vars, lateralisation_vars, anatomical_regions


# main function is QUERY_LATERALISATION



def gifs_lat(gif_lat_file):
    """
    factor function. opens the right/left gif parcellations from excel and extracts the right/left gifs as series/list.
    """
    gifs_right = gif_lat_file.loc[gif_lat_file['R'].notnull(), 'R']
    gifs_left = gif_lat_file.loc[gif_lat_file['L'].notnull(), 'L']

    return gifs_right, gifs_left


def QUERY_LATERALISATION(inspect_result, df, map_df_dict, gif_lat_file,
                       side_of_symptoms_signs=None,
                       pts_dominant_hemisphere_R_or_L=None,
                       normalise_lat_to_loc=False):
    """
    After obtaining inspect_result and clinician's filter, can optionally use this function to determine
    lateralisation e.g. for EpiNav(R) visualisation.

    Run this after QUERY_SEMIOLOGY OR QUERY_INTERSECTION_TERMS

    inspect_result may not have a lateralising column (if all were NaNs)
    goes through row by row

    ---
    > inspect_result is obtained from QUERY_SEMIOLOGY OR QUERY_INTERSECTION_TERMS
    > df as per pivot_result_to_pixel_intensities's df
    > side_of_symptoms_signs: 'R' or 'L' - side of symptoms/signs on limbs
    > pts_dominant_hemisphere_R_or_L: if known from e.g. fMRI language 'R' or 'L'

    returns all_combined_gifs which is similar in structure to output of pivot_result_to_one_map (final step),
        but in this case, the output column is pt #s rather than pixel intensity.
    Should then run this again through a similar process as
        pivot_result_to_pixel_intensity to curve fit (QuantileTransformer or chi2)
    ---

    Alim-Marvasti Aug 2019
    """

    lat_vars = [i for i in lateralisation_vars() if i not in ['Lateralising']]

    #check there is lateralising value
    try:
        Lat = inspect_result['Lateralising']
        logging.debug(f'Lateralisation based on: {Lat.sum()} datapoints')

    except KeyError:
        print('No Lateralising values found for this query of the database.')
        return

    # check that the lateralising columns isn't null where it shouldn't be i.e. CL/IL/DomH/NonDomH not null:
    # but not 'BL (Non-lateralising)'
    # first ensure other columns all feature in this inspect_result:
    inspect_result2 = inspect_result.copy()
    for col in lat_vars:
        if col not in inspect_result2.columns:
            inspect_result2[col] = np.nan
    #now can check lateralising columns isn't null where it shouldn't be:
    missing_lat = inspect_result2.loc[(inspect_result2['CL'].notnull())|
                                    (inspect_result2['IL'].notnull())|
                                    (inspect_result2['DomH'].notnull())|
                                    (inspect_result2['NonDomH'].notnull()), :]
    missing_lat_null_mask = missing_lat['Lateralising'].isnull()
    if not missing_lat_null_mask.all():
        logging.debug('\nNo missing Lateralising data points.')
    else:  # semiology term not recognised
        logging.warning('The inspect_result lat col has NaNs/zero where it should not: autofilled')
        df_of_missing_lats = missing_lat.loc[missing_lat_null_mask]
        df.loc[df_of_missing_lats.index, 'Lateralising'] = df_of_missing_lats[['CL', 'IL', 'DomH', 'NonDomH']].sum(axis=1)

    # check columns exist (not removed in preceding notnull steps from other functions):
    for col in lat_vars:
        if col not in inspect_result.columns:
            inspect_result[col] = 0


    # summarise overall lat values
    IL = inspect_result['IL']
    CL = inspect_result['CL']
    DomH = inspect_result['DomH']
    NonDomH = inspect_result['NonDomH']
    BL = inspect_result['BL (Non-lateralising)']

    logging.debug(f'Overall Contralateral: {CL.sum()} datapoints')
    logging.debug(f'Ipsilateral: {IL.sum()} datapoints')
    logging.debug(f'Bilateral/Non-lateralising: {BL.sum()} datapoints. This is not utilised in our analysis/visualisation.')
    logging.debug(f'Dominant Hemisphere: {DomH.sum()} datapoints')
    logging.debug(f'Non-Dominant Hemisphere: {NonDomH.sum()} datapoints')


    # initialise:
    Right = 0
    Left = 0
    inspect_result_lat = inspect_result.loc[inspect_result['Lateralising'].notnull(), :]  # only those with lat
    no_rows = inspect_result_lat.shape[0]

    # ensure there is patient's lateralised signs and check dominant known or not
    if not side_of_symptoms_signs:
        print('Please retry and determine side_of_symptoms_signs argument')
        return

    # cycle through rows of inspect_result_lat:
    id_cols = [i for i in full_id_vars() if i not in ['Localising']]  # note 'Localising' is in id_cols

    for i in range (no_rows):
        logging.debug(str(i))
        Right = 0
        Left = 0

        full_row = inspect_result_lat.iloc[[i],:]
        row = full_row.drop(labels=id_cols, axis='columns', inplace=False, errors='ignore')
        row = row.dropna(how='all', axis='columns')
        # row = row.dropna(how='all', axis='rows')

        one_map = big_map(map_df_dict)
        row_to_one_map = pivot_result_to_one_map(row, one_map, raw_pt_numbers_string='pt #s',
                                                suppress_prints=True)
        # ^ row_to_one_map now contains all the lateralising gif parcellations


        # some pts will have lateralising but no localising values:
        if ( ('Localising' not in full_row.columns) | (full_row['Localising'].sum() ==0) ):
            logging.debug('\nsome of the extracted lateralisation have no localisation - for now these are ignored but re-inspect!')
            logging.debug(f'row# = {i}')
            # probably, in future, instead of break we want to compare this row's:
            # full_row['Lateralising']    to the overall    inspect_result['Lateralising']    and use that proportion
            continue

        # set the scale of influence of lateralisation on the gif parcellations:
        proportion_lateralising = full_row['Lateralising'].sum() / full_row['Localising'].sum()

        if proportion_lateralising > 1:
            proportion_lateralising = 1
            logging.debug('some extracted lateralising data exceed the localising data,')
            logging.debug('for now these are taken as proportion_lateralising=1.0 !')

        # check columns exist in this particular row:
        for col in lat_vars:
            if col not in row.columns:
                row[col] = 0
            else:
                continue

        # summarise overall lat values
        IL_row = row['IL'].sum()
        CL_row = row['CL'].sum()
        DomH_row = row['DomH'].sum()
        NonDomH_row = row['NonDomH'].sum()
        BL_row = row['BL (Non-lateralising)'].sum()

        # pt input
        if side_of_symptoms_signs == 'R':
            Right += IL_row
            Left += CL_row

        elif side_of_symptoms_signs == 'L':
            Right += CL_row
            Left += IL_row

        if pts_dominant_hemisphere_R_or_L:
            if pts_dominant_hemisphere_R_or_L == 'R':
                Right += DomH_row
                Left += NonDomH_row
            elif pts_dominant_hemisphere_R_or_L =='L':
                Right += NonDomH_row
                Left += DomH_row

        Total = Right+Left
        if Right == Left:
            # no point as this is 50:50 as it already is, so skip
            continue

        # now should be able to use above to lateralise the localising gif parcellations:
        # if there are 100 localisations in one row, and only 1 IL And 3 CL, it would be too much
        # to say the IL side gets one third of the CL side as number of lat is too low
        # hence normalise by dividing by proportion_lateralising (which is between (0,1])

        gifs_right, gifs_left = gifs_lat(gif_lat_file)
#         row_to_one_map
#         proportion_lateralising
#         Right, Left

        # find lowest value of R or L
        lower_postn = np.argmin([Right, Left])
        if lower_postn == 0:
            isin = gifs_right  # reduce right sided intensities/pt #s
        elif lower_postn == 1:
            isin = gifs_left

        lower_value = [Right, Left][lower_postn]
        higher_value = [Right, Left]
        higher_value.remove(lower_value)

        ratio = lower_value / Total

        if normalise_lat_to_loc==True:
            norm_ratio = ratio / proportion_lateralising  # see comments on section above about why we should normalise
            if norm_ratio > 1:
                norm_ratio = 1
                print('norm_ratio capped at 1: small proportion of data lateralised')
        elif normalise_lat_to_loc==False:
            norm_ratio = lower_value / higher_value


        # if proportion_lateralising is 1, straightforward: return dataframe of right/left gifs whichever lower
        df_lower_lat_to_be_reduced = row_to_one_map.loc[row_to_one_map['Gif Parcellations'].isin(list(isin))]
        # now make these values lower by a proportion = norm_ratio (in this case norm_ratio = ratio as denom is 1)
        reduce_these = df_lower_lat_to_be_reduced.loc[:,'pt #s']
        df_lower_lat_to_be_reduced.loc[:,'pt #s'] = norm_ratio * reduce_these
        # re attribute these corrected reduced lateralised values to the entire row's data:
        row_to_one_map.loc[df_lower_lat_to_be_reduced.index, :] = df_lower_lat_to_be_reduced

        # now need to merge/concat these rows-(pivot-result)-to-one-map as the cycle goes through each row:
        if i == 0:
            # can't merge first row
            all_combined_gifs = row_to_one_map
            logging.debug('end of zeroo')
            continue
        elif i != 0:
            all_combined_gifs = pd.concat([all_combined_gifs, row_to_one_map], join='outer', sort=False)
        logging.debug(f'end of i {i}')


    # if EpiNav doesn't sum the pixel intensities: (infact even if it does)
    fixed = all_combined_gifs.pivot_table(columns='Gif Parcellations', values='pt #s', aggfunc='sum')
    fixed2 = fixed.melt(value_name='pt #s')
    fixed2.insert(0, 'Semiology Term', np.nan)
    # fixed2.loc[0, 'Semiology Term'] = str( list(inspect_result.index.values) )
    all_combined_gifs = fixed2
    all_combined_gifs

    return all_combined_gifs.round()
