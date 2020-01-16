from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# needed for querying dataframe localisations, Transforming and mapping to EpiNav gif parcellations
from mega_analysis.crosstab.mega_analysis.MEGA_ANALYSIS import *
from mega_analysis.crosstab.mega_analysis.QUERY_SEMIOLOGY import *
from mega_analysis.crosstab.mega_analysis.QUERY_INTERSECTION_TERMS import QUERY_INTERSECTION_TERMS
from mega_analysis.crosstab.mega_analysis.melt_then_pivot_query import *
from mega_analysis.crosstab.mega_analysis.pivot_result_to_pixel_intensities import *

# needed to collate lateralisation data
from mega_analysis.crosstab.mega_analysis.QUERY_LATERALISATION import *
from mega_analysis.crosstab.mega_analysis.lateralised_intensities import lateralisation_to_pixel_intensities
from mega_analysis.crosstab.mega_analysis.pivot_result_to_pixel_intensities import *

# mapping to gif
from mega_analysis.crosstab.mega_analysis.mapping import mapping, big_map, pivot_result_to_one_map


def get_scores(semiology_term='Head version', output_path=None):
    repo_dir = Path(__file__).parent.parent
    resources_dir = repo_dir / 'resources'
    excel_path = resources_dir / 'syst_review_single_table.xlsx'
    semiology_dict_path = resources_dir / 'semiology_dictionary.yaml'

    # I recommend keep this to True
    use_semiology_dictionary = True

    # # LATERALISATION initilisation

    # I reconmend minmaxscaler. The previous example used non-linear which you have the visualisations for (Rachel did)
    # method = 'non-linear'
    method = 'min_max'
    # method = 'linear'
    # method = 'chi2-dist'

    scale_factor = 15
    quantiles = 100
    if method in ('non-linear', 'nonlinear'):
        raw_pt_numbers_string = 'normal QuantileTransformer'
    else:
        raw_pt_numbers_string = str(method)
    intensity_label = 'Lateralised Intensity. '+str(raw_pt_numbers_string)+'. '+'quantiles: '+str(quantiles)+'. '+'scale: '+str(scale_factor)

    df, df_ground_truth, df_study_type = MEGA_ANALYSIS(excel_data=excel_path)

    inspect_result = QUERY_SEMIOLOGY(
        df,
        semiology_dict_path,
        semiology_term=semiology_term,
        use_semiology_dictionary=use_semiology_dictionary,
    )


    # # 2.3 QUERY_LATERALISATION
    all_combined_gifs = QUERY_LATERALISATION(
        inspect_result,
        df,
        excel_path,
        side_of_symptoms_signs='R',
        pts_dominant_hemisphere_R_or_L='L',
    )

    all_lateralised_gifs = lateralisation_to_pixel_intensities(
        all_combined_gifs,
        df,
        semiology_term,
        quantiles,
        method=method,
        scale_factor=scale_factor,
        intensity_label=intensity_label,
        use_semiology_dictionary=use_semiology_dictionary,
    )

    array = np.array(all_lateralised_gifs)
    labels = array[:, 1].astype(np.uint16)
    scores = array[:, 3].astype(np.float32)
    scores_dict = {int(label): float(score) for (label, score) in zip(labels, scores)}

    if output_path is not None:
        df = pd.DataFrame(scores_dict.items(), columns=['Label', 'Score'])
        df.to_csv(output_path, index=False)

    return scores_dict
