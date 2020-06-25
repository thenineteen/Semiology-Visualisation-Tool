temporal_postcodes = {
    'TL': [
        'Anterior (temporal pole)',
        'Lateral Temporal',
        'Mesial Temporal',
        'Posterior Temporal',
        'Basal (including Fusiform OTMG)',
    ],
    'Basal (including Fusiform OTMG)': [
        'OTMG (fusiform)',
    ],
    'Mesial Temporal': [
        'Ant Mesial Temporal',
        'Post Mesial Temporal',
        'Enthorinal Cortex',
        'Fusiform',
        'AMYGD',
        'PARAHIPPOCAMPUS',
        'HIPPOCAMPUS',
    ],
    'Lateral Temporal': [
        'STG (includes Transverse Temporal Gyrus, Both Planum)',
        'MTG',
        'ITG',
    ],
    'STG (includes Transverse Temporal Gyrus, Both Planum)': [
        'Transverse Temporal Gyrus (Heschl\'s, BA 41,  42, ?opercula)',
        'Planum Temporale',
        'Planum Polare',
    ],
}

frontal_postcodes = {
    'FL': [
        'frontal pole',
        'Pre-frontal (BA 8, 9, 10, 11, 12, 13, 14, 24, 25, 32, 44, 45, 46, 47)',
        'Medial Frontal\n(should include medial premotor and its constituents as its subsets)',
        'Primary Motor Cortex (Pre-central gyrus, BA 4, Rolandic)',
        'SFG (F1)',
        'MFG (F2)',
        'IFG (F3)\n(BA 44,45,47)',
        'Premotor frontal (posterior frontal)',
        'SMA (pre-central gyrus; posterior SFG, MFG)',
        'SSMA',
    ],
    'Pre-frontal (BA 8, 9, 10, 11, 12, 13, 14, 24, 25, 32, 44, 45, 46, 47)': [
        'DL-PFC\n(BA 46)\n(include subgroups BA 9, 8, 10 - frontopolar/anterior prefrontal)',
        'gyrus rectus (basal = gyrus rectus and OFC)',
        'Orbito-frontal (BA 10, 11, 12/47) (basal = gyrus rectus and OFC)',
    ],
    'Primary Motor Cortex (Pre-central gyrus, BA 4, Rolandic)': [
        'medial precentral',
        'Rolandic Operculum (low BA4)',
    ],
    'SFG (F1)': [
        'Med SFG',
        'Ant SFG',
    ],
    'MFG (F2)': [
        'Ant MFG',
    ],
    'IFG (F3)\n(BA 44,45,47)': [
        'Pars orbitalis (subgroup of IFG)\n(BA 47)',
        'Pars Triangularis (subgroup IFG)',
        'Pars opercularis (BA 44)(subgroup IFG, ?opercula)',
    ],
    'Premotor frontal (posterior frontal)': [
        'Ant Premotor\n(BA 8, frontal-eye-fields)',
        'Lateral Premotor\n(BA 6)',
        'Medial Premotor (including pre SMA)',
    ],
    'Orbito-frontal (BA 10, 11, 12/47) (basal = gyrus rectus and OFC)': [
        'Ant OF',
        'Post OF',
        'Lat OF',
        'Med OF',
    ],
    'Lateral Premotor\n(BA 6)': [
        'Ventro-lateral premotor',
        'Dorso-lateral premotor',
    ]
}

cingulate_postcodes = {
    'CING': [
        'Cingulum WM',
        'Ant Cing',
        'Middle Cingulate',
        'Post Cing',
        'Isthmus',
    ],
    'Ant Cing': [
        'Ventr Ant Cing\n(BA 24)',
        'Dorsal Ant Cing (BA 32)',
    ]
}

parietal_postscodes = {
    'PL': [
        'Primary Sensory Cortex (post-central gyrus)',
        'Sup. pariet. lobule',
        'Inferior Parietal Lobule',
    ],
    'Primary Sensory Cortex (post-central gyrus)': [
        'medial anterior parietal',
    ],
    'Sup. pariet. lobule': [
        'Precuneus (medial post sup parietal lobule)',
    ],
    'Inferior Parietal Lobule': [
        'Supramarg gyrus (post part of parietal operculum)',
        'Angular gyrus (BA 39)',
        'parietal operculum (ceiling of secondary somatosensory cortex)',
    ]
}

occipital_postcodes = {
    'OL': [
        'Cuneus ',
        'Mesial Occipital',
        'Lateral Occipital',
        'Posterior Occipital Gyrus',
    ],
    'Mesial Occipital': [
        'Lingual gyrus ',
    ]
}

insular_postcodes = {
    'INSULA': [
        'Ant Ins',
        'Precentral gyrus',
        'Postcentral gyrus',
        'Posterior long gyrus',
        'Insular pole',
    ]
}

cerebellar_postcodes = {
    'Cerebellum': [
        'Hemisphere',
        'Vermis',
    ]
}


def postcode_dictionaries(**kwargs):
    """
    Combine dictionaries for hierarchy reversals.
    The kwargs are allowed in single use only. Called by Hierarchy Class.
    Hypothalamus has no key:value pairs.
    """
    if 'temporal' in kwargs:
        return temporal_postcodes
    if 'frontal' in kwargs:
        return frontal_postcodes
    if 'cingulate' in kwargs:
        return cingulate_postcodes
    if 'parietal' in kwargs:
        return parietal_postscodes
    if 'occipital' in kwargs:
        return occipital_postcodes
    if 'insular' in kwargs:
        return insular_postcodes
    if 'cerebellar' in kwargs:
        return cerebellar_postcodes

    else:
        postcodes = {**temporal_postcodes, **frontal_postcodes,
                     **cingulate_postcodes, **parietal_postscodes, **occipital_postcodes, **insular_postcodes, **cerebellar_postcodes}
        return postcodes
