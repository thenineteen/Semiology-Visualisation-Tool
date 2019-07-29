import pandas as pd

def melt_then_pivot_query(df, inspect_result, semiology_term):

    """
    if happy all are the same semiology, after insepction of QUERY_SEMIOLOGY, melt then pivot_table:

        ---
        inspect_result is a df
    """

    # find all localisation columns present:
    localisation_labels = df.columns[17:72]
    relevant_localisations = [cols for cols in inspect_result.columns if cols in localisation_labels]


    # MELT
    #first determine id_vars:
    full_id_vars = ['Reference', 'Relevant Tot Sample', 'Tot Pt included',
                    'Reported Semiology', 'Semiology Category', 'Ground truth description',
                    'Post-op Sz Freedom (Engel Ia, Ib; ILAE 1, 2)',
                'Concordant Neurophys & Imaging (MRI, PET, SPECT)',
                'sEEG and/or ES',
                'Lateralising', 'CL', 'IL', 'BL (Non-lateralising)', 'DomH', 'NonDomH',
                'Localising',
                    '# tot pt in the paper', '# pt excluded', '# pt sz free post-surg',
                'Spontaneous Semiology (SS)', 'Epilepsy Topology (ET)', 'Cortical Stimulation (CS)', 'Other (e.g. Abs)']
    id_vars_present_in_query = [cols for cols in inspect_result.columns if cols in full_id_vars]

    inspect_result_melted = inspect_result.melt(id_vars=id_vars_present_in_query, value_vars=relevant_localisations, 
                                var_name='melted_variable', value_name='melted_numbers')

    # replace NaNs with 0s as melting creates many:
    inspect_result_melted.fillna(value=0, inplace=True)


    # PIVOT_TABLE
    inspect_result_melted['pivot_by_column'] = semiology_term
    pivot_result = inspect_result_melted.pivot_table(index='pivot_by_column', columns='melted_variable', values='melted_numbers', aggfunc='sum')

    return pivot_result