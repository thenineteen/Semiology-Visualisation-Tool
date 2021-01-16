import numpy as np
import pandas as pd
import copy
import statsmodels.stats.proportion as ssp
import multinomial_ci

def get_counts_df(query_results, region_names, merge_temporal = False, other_included = True):
    """
        Converts query results to matrix of counts by semiology and localisation
        
        Inputs
        - query_results: a dictionary where keys are semiologies and values are
        'query_inspection' for that semiology, as returned by QUERY_SEMIOLOGY
        - Requires region_names, a dictionary of defined groups of localisations
        - *merge_temporal: False if want to break down top level label TL into anterior,
        posterior etc.
        - *other_included: True if want to keep all top level localisation columns. False
        will drop interlobar junctions etc.

        Returns
        - counts_df: a matrix where columns are localisations and index are
        semiologies, where the values are the number of datapoints corresponding to that
        localisation and semiology
    """
    columns_of_interest = []
    counts_matrix = []
    for semiology, value in query_results.items():
        query_inspection = value['query_inspection']
        if merge_temporal == False:
            columns_of_interest = (region_names['low_level_temporal_of_interest'] + region_names['of_interest_minus_tl'])
        else:
            columns_of_interest = copy.deepcopy(region_names['of_interest'])
        if other_included:
            columns_of_interest += region_names['top_level_all_other']
        semiology_counts = query_inspection[columns_of_interest].sum().values
        counts_matrix.append(semiology_counts)
    counts_df = pd.DataFrame(counts_matrix, index=query_results.keys(), columns=columns_of_interest)
    return counts_df


def merge_all_other_semiologies(counts_df, semiologies_of_interest):
    """
        Merges semiologies other than the specified semiologies of interest into an "All other" row
    """
    of_interest_mask = counts_df.index.isin(semiologies_of_interest)
    to_merge_df = counts_df.loc[~of_interest_mask]
    to_merge_df_sum = to_merge_df.sum(0)
    dropped_df = counts_df.drop(to_merge_df.index, 'index')
    dropped_df.loc['All other'] = to_merge_df_sum
    return dropped_df

def merge_all_other_zones(counts_df, roi):
    """
        Merges localisations other than the specified regions of interest into an "All other" column
    """
    of_interest_mask = counts_df.columns.isin(roi)
    to_merge_df = counts_df.loc[:,~of_interest_mask]
    to_merge_df_sum = to_merge_df.sum(1)
    dropped_df = counts_df.drop(to_merge_df.columns, 'columns')
    dropped_df['All other'] = to_merge_df_sum
    return dropped_df

def calculate_proportions(counts_df, axis):
    """
        Calculate  proportions from counts_df, 
    """
    if axis == 'semiology':
        totals_by_semiology = counts_df.sum(1)
        proportions_df = counts_df.div(totals_by_semiology, axis='index')
    elif axis == 'zone':
        totals_by_zone = counts_df.sum(0)
        proportions_df = counts_df.div(totals_by_zone, axis='columns')
    else:
        raise ValueError('axis must be given from {semiology, zone}')
    return proportions_df\

def calculate_confint(counts_df, axis = 'semiology', method = 'binomial', alpha=0.05):
    """
        Calculate confidence intervals of proportions from counts_df

        Inputs:
        - method: from {binomial, sison-glaz, goodman}
        - axis: calculate proportion CI by semiology or by zone
        - alpha
    """
    if axis == 'semiology':
        pass
    elif axis == 'zone':
        counts_df = counts_df.T
    else:
        raise ValueError('axis must be given from {semiology, zone}')

    ci_matrix = []
    n_rows, n_columns = counts_df.shape
    for nth_row in range(n_rows):
        vector = counts_df.iloc[nth_row, :]
        if method == 'binomial':
            ci_row = ssp.proportion_confint(vector, sum(vector), alpha=alpha, method='wilson')
            ci_matrix.append(np.array(ci_row).T)
        elif method == 'sison-glaz':
            ci_row = multinomial_ci.sison(vector, alpha=alpha)
            ci_matrix.append(ci_row)
        elif method == 'goodman':
            ci_row = ssp.multinomial_proportions_confint(vector, method='goodman', alpha=alpha)
            ci_matrix.append(ci_row)
        else:
            raise ValueError('axis must be given from {binomial, sison-glaz, goodman}')
            
    ci_matrix = np.array(ci_matrix)
    lower_ci_df = pd.DataFrame(ci_matrix[:,:,0], index=counts_df.index, columns=counts_df.columns)
    upper_ci_df = pd.DataFrame(ci_matrix[:,:,1], index=counts_df.index, columns=counts_df.columns)
    
    return lower_ci_df, upper_ci_df


def summarise_query(query_results, axis, region_names, confint_method = 'binomial',
                    merge_temporal = False, other_regions_included = True,
                    semiologies_of_interest = None, regions_of_interest = None,
                    drop_other_semiology = True):

    """
        Wrapper function combining get_counts_df, merge_all_other_semiologies, merge_all_other_zones, 
        calculate_confint.

        Returns a dictionary containing:
            counts
            proportion
            confints - list, first df is lower confidence interval and second is upper
    """
    counts_df = get_counts_df(query_results, region_names, merge_temporal, other_regions_included)
    if semiologies_of_interest:
        counts_df = merge_all_other_semiologies(counts_df, semiologies_of_interest)
        if drop_other_semiology:
            counts_df = counts_df.drop('All other')
    if regions_of_interest:
        counts_df = merge_all_other_zones(counts_df, regions_of_interest)
    proportion_df = calculate_proportions(counts_df, axis)
    confint_dfs = calculate_confint(counts_df, axis = axis, method = confint_method, alpha=0.05)
    processed_dfs = {
        'counts': counts_df,
        'proportion': proportion_df,
        'confints': confint_dfs
    }
    return processed_dfs