import pandas as pd
from ..semiology_all_localisations import all_localisations


# note 'Localising' is in id_cols not localisation_labels

def full_id_vars():
    id_cols = ['Reference', 'Relevant Tot Sample', 'Tot Pt included',
                'Reported Semiology', 'Semiology Category', 'Ground truth description',
                'Post-op Sz Freedom (Engel Ia, Ib; ILAE 1, 2)',
                'Concordant Neurophys & Imaging (MRI, PET, SPECT)',
                'sEEG and/or ES',
                'Localising', 'Reported Localisation',
                'padeiatric? <7 years (0-6 yrs) y/n',
                '# tot pt in the paper', '# pt excluded', '# pt sz free post-surg',
                'Spontaneous Semiology (SS)', 'Epilepsy Topology (ET)', 'Cortical Stimulation (CS)', 'Other (e.g. Abs)']

    return id_cols


def lateralisation_vars():
    lat_vars = ['Lateralising', 'CL', 'IL', 'BL (Non-lateralising)', 'DomH', 'NonDomH']

    return lat_vars


def anatomical_regions(df):
    """
    After cleaning in MEGA_ANALYSIS, the df will have lost some localisation columns.
    Full localisation names are in all_localisations().
    Improved version from:
    "localisation_labels = df.columns[17:88]  # May 2020 17:72  to 17:88"
    """
    all_localisations_list = all_localisations()
    localisation_labels = [i for i in df.columns if i in all_localisations_list]

    return localisation_labels