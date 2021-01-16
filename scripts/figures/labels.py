from mega_analysis.crosstab.lobe_top_level_hierarchy_only import top_level_lobes
from mega_analysis.crosstab.hierarchy_dictionaries import temporal_postcodes

def get_region_names():
    top_level = top_level_lobes()
    top_level_of_interest = [
                            'TL',
                            'FL',
                            'PL',
                            'OL',
                            'INSULA',
                            'CING',
                            'Hypothalamus',
                            ]
    top_level_all_other = list(set(top_level) - set(top_level_of_interest))
    top_level_of_interest_minus_tl = list(set(top_level_of_interest) - set(['TL']))

    low_level_temporal_all =  [y for x in temporal_postcodes.values() for y in x]
    low_level_temporal_of_interest = ['Anterior (temporal pole)',
                                    'Lateral Temporal',
                                    'Mesial Temporal',
                                    'Posterior Temporal',
                                    'Basal (including Fusiform OTMG)']

    all_regions = get_all_regions()

    region_names = {'all': all_regions,
                    'top_level': top_level,
                    'of_interest': top_level_of_interest,
                    'of_interest_minus_tl': top_level_of_interest_minus_tl,
                    'top_level_all_other': top_level_all_other,
                    'top_level_temporal': ['TL'],
                    'low_level_temporal_all': low_level_temporal_all,
                    'low_level_temporal_of_interest': low_level_temporal_of_interest}

    return region_names

def clean_localisations(labels):
    pre_localisation = ['Anterior (temporal pole)',
             'Lateral Temporal',
             'Mesial Temporal',
             'Posterior Temporal',
             'Basal (including Fusiform OTMG)',
             'Hypothalamus',
             'PL',
             'CING',
             'OL',
             'FL',
             'INSULA',
             'All other']

    post_localisation = ['Anterior Temporal',
     'Lateral Temporal',
     'Mesial Temporal',
     'Posterior Temporal',
     'Basal Temporal',
     'Hypothalamus',
     'Parietal Lobe',
     'Cingulate Gyrus',
     'Occipital Lobe',
     'Frontal Lobe',
     'Insula',
     'Interlobar Junctions+']

    look_up_dict = dict(zip(pre_localisation, post_localisation))

    return [look_up_dict[label] for label in labels]


def clean_semiologies(labels):
    pre_semiology = ['Epigastric', 'Fear-Anxiety', 'Psychic', 'Autonomous-Vegetative',
       'Olfactory', 'Visual - Elementary', 'Somatosensory',
       'Non-Specific Aura', 'Head or Body Turn', 'Head Version', 'Tonic',
       'Dystonic', 'Clonic', 'Hypermotor', 'Complex Behavioural',
       'Automatisms Combination - Manual LowerLimb Oral',
       'Vocalisation: Unintelligible Noises', 'Aphasia',
       'Ictal Speech: Formed Words', 'Dialeptic/LOA', 'All other']
    
    post_semiology = ['Epigastric', 'Fear-Anxiety', 'Psychic', 'Autonomic',
       'Olfactory', 'Visual - Elementary', 'Somatosensory',
       'Non-Specific Aura', 'Head or Body Turn', 'Head Version', 'Tonic',
       'Dystonic', 'Clonic', 'Hypermotor', 'Complex Behavioural',
       'Automatisms','Unintelligible Noises', 'Aphasia',
       'Ictal Speech: Formed Words', 'Dialeptic/LOA', 'All other']

    look_up_dict = dict(zip(pre_semiology, post_semiology))

    return [look_up_dict[label] for label in labels]


def get_all_regions():
    all_regions = """TL
Anterior (temporal pole)
Lateral Temporal
STG (includes Transverse Temporal Gyrus, Both Planum)
Transverse Temporal Gyrus (Heschl's, BA 41,  42, ?opercula)
Planum Temporale
Planum Polare
MTG
ITG
Mesial Temporal
Ant Mesial Temporal
Post Mesial Temporal
Enthorinal Cortex
Fusiform
AMYGD
PARAHIPPOCAMPUS
HIPPOCAMPUS
Posterior Temporal
Basal (including Fusiform OTMG)
OTMG (fusiform)
FL
frontal pole
Pre-frontal (BA 8, 9, 10, 11, 12, 13, 14, 24, 25, 32, 44, 45, 46, 47)
DL-PFC (BA 46) (include subgroups BA 9, 8, 10 - frontopolar/anterior prefrontal)
gyrus rectus (basal = gyrus rectus and OFC)
Orbito-frontal (BA 10, 11, 12/47) (basal = gyrus rectus and OFC)
Post OF
Lat OF
Med OF
Medial Frontal (include medial premotor and its constituents as its subsets)
Primary Motor Cortex (Pre-central gyrus, BA 4, Rolandic)
medial precentral
Rolandic Operculum (low BA4)
SFG (F1)
Med SFG
Post SFG
Ant SFG
MFG (F2)
Ant MFG
Mid MFG
Post MFG
Pars Triangularis (subgroup IFG)
Pars opercularis (BA 44)(subgroup IFG, ?opercula)
Premotor frontal (posterior frontal)
Ant Premotor (BA 8, frontal-eye-fields)
Medial Premotor (including pre SMA)
SMA (pre-central gyrus; posterior SFG, MFG)
SSMA
CING
Cingulum (WM)
Ant Cing (frontal, genu)
Dorsal Ant Cing (BA 32)
Middle Cingulate
Post Cing
Isthmus
PL
Primary Sensory Cortex (post-central gyrus)
medial anterior parietal
Sup. pariet. lobule
Precuneus (medial post sup parietal lobule)
Inferior Parietal Lobule
Supramarg gyrus (post part of parietal operculum)
Angular gyrus (BA 39)
parietal operculum (ceiling of secondary somatosensory cortex)
OL
Mesial Occipital
Lingual gyrus  (medial and basal)
Cuneus
Lateral Occipital (SOG, IOG, LOG)
Posterior Occipital Gyrus
Superior Occipital Gyrus
INSULA
Ant Ins
Anterior Short Gyrus
Middle Short Gyrus
Post short gyrus
Precentral gyrus
Postcentral gyrus
Posterior long gyrus
Hypothalamus
Sub-Callosal Cortex
Cerebellum
Hemisphere
Vermis
FT
TO
TP
FTP
TPO Junction
PO
FP
Perisylvian""".splitlines()

    all_regions += ['''IFG (F3)
(BA 44,45,47)''',
    '''Lateral Premotor
(BA 6)''',
    '''Pars orbitalis (subgroup of IFG)
(BA 47)''']
    # '''Pars opercularis (BA 44)(subgroup IFG, ?opercula)'''

    return all_regions