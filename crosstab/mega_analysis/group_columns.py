import pandas as pd 



# note 'Localising' is in id_cols not localisation_labels

def full_id_vars():
    id_cols = ['Reference', 'Relevant Tot Sample', 'Tot Pt included',
                    'Reported Semiology', 'Semiology Category', 'Ground truth description',
                    'Post-op Sz Freedom (Engel Ia, Ib; ILAE 1, 2)',
                'Concordant Neurophys & Imaging (MRI, PET, SPECT)',
                'sEEG and/or ES',
                'Localising', 'Reported Localisation',
                    '# tot pt in the paper', '# pt excluded', '# pt sz free post-surg',
                'Spontaneous Semiology (SS)', 'Epilepsy Topology (ET)', 'Cortical Stimulation (CS)', 'Other (e.g. Abs)']
    
    return id_cols


def lateralisation_vars():
    lat_vars = ['Lateralising', 'CL', 'IL', 'BL (Non-lateralising)', 'DomH', 'NonDomH']

    return lat_vars


def anatomical_regions(df):
    localisation_labels = df.columns[17:72]  # for July 2019 version at least

    return localisation_labels