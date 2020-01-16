import pandas as pd
from .group_columns import full_id_vars, lateralisation_vars, anatomical_regions


def melt_then_pivot_query(df, inspect_result, semiology_term):

    """
    if happy all are the same semiology, after insepction of QUERY_SEMIOLOGY, melt then pivot_table:

        ---
        inspect_result is a df
    Ali Alim-Marvasti July 2019
    """

    # find all localisation columns present:
    localisation_labels = anatomical_regions(df)
    relevant_localisations = [cols for cols in inspect_result.columns if cols in localisation_labels]


    # MELT
    #first determine id_vars: in this case we don't use lateralisation add that too
    full_id_cols = full_id_vars() + lateralisation_vars()

    id_vars_present_in_query = [cols for cols in inspect_result.columns if cols in full_id_cols]

    inspect_result_melted = inspect_result.melt(id_vars=id_vars_present_in_query, value_vars=relevant_localisations,
                                var_name='melted_variable', value_name='melted_numbers')

    # replace NaNs with 0s as melting creates many:
    inspect_result_melted.fillna(value=0, inplace=True)


    # PIVOT_TABLE
    inspect_result_melted['pivot_by_column'] = semiology_term
    pivot_result = inspect_result_melted.pivot_table(index='pivot_by_column', columns='melted_variable', values='melted_numbers', aggfunc='sum')

    # sort the columns of the pivot_table by ascending value:
    pivot_result.sort_values(by=semiology_term, axis=1, inplace=True, ascending=False)

    return pivot_result
