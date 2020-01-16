import pandas as pd
from .pivot_result_to_pixel_intensities import *

def lateralisation_to_pixel_intensities(all_combined_gifs, df,
                                        semiology_term,
                                        quantiles, method='non-linear', scale_factor=10,
                                        intensity_label='lateralised intensity',
                                        use_semiology_dictionary=False,
                                        plot=False):
    """
    runs pivot_result_to_pixel_intensities when the input has already been mapped to gifs as a result of
    running QUERY_LATERALISATION.
    This is the final step in the query_lateralisation pathway.

    Alim-Marvasti Aug 2019
    """
    # isn't really a pivot_result but let's use consistent notations:
    pivot_result = all_combined_gifs[['pt #s']].T
    all_combined_gifs_intensities = pivot_result_to_pixel_intensities(pivot_result, df,
                                      method=method, scale_factor=scale_factor, quantiles=quantiles,
                                      use_main_df_calibration=False, plot=plot)

    # now we just need to transpose it and add the other columns back
    a2 = all_combined_gifs[['Gif Parcellations']].T
    a3 = all_combined_gifs[['Semiology Term']].T
    all_combined_gifs_intensities.index = [intensity_label]

    all_lateralised_gifs = pd.concat([a3, a2, pivot_result, all_combined_gifs_intensities], sort=False).T

    all_lateralised_gifs.loc[0, 'Semiology Term'] = str(semiology_term)
    all_lateralised_gifs.loc[1, 'Semiology Term'] = 'use_semiology_dictionary='+str(use_semiology_dictionary)


    return all_lateralised_gifs
