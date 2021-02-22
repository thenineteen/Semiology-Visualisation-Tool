import pandas as pd

from mega_analysis.semiology import Semiology, Laterality


def marginal_GIF_probabilities(all_combined_gifs):
    """
    Input the DataFrame of GIF Parcellations and values for all semiologies.
        all_combined_gifs: GIF values
            all_combined_gifs is a heatmap df i.e. from patient.get_num_datapoints_dict()  # for all data not for single semiology
            remember the cols of all_combined_gifs are "Gif Parcellations" and "pt #s"

    Returns the marginal_probabilities.

    Future: As sensitivity analyses, should check the variance of marginal prob when using different filters
        concretely: marginal_p should be using all the data without filters, but then when using filters, see if we
        had used a filtered df using one of the exclusions (e.g. EZ only or based on age),
        how much would the marginal_p differ and Bayesian inference vary by?

    Alim-Marvasti Feb 2021
    """

    # Localisations
    gif_df = all_combined_gifs.copy()
    gif_df = gif_df.fillna(0)
    gif_df['pt #s'] = gif_df['pt #s'] / (gif_df['pt #s'].sum())
    marginal_GIF_prob = gif_df

    return marginal_GIF_prob


def marginal_Localisation_and_Semiology_probabilities(df):
    """ Returns the marginal localisation and semiology probabilities

    df: preprocessed Semio2Brain DataFrame obtained from MEGA_ANALYSIS after hierarchy reversal.
        df = MEGA_ANALYSIS()  # for all-data
        also used SemioDict
        df = hierarchy_reversal()
            Assume df is the fully cleaned and hierarchy reversed Semio2Brain descriptions.

        I.e. Use the notebook from forest plot branch to get df of semiology by localisation as all of above is already done.
        rows: semiologies
        columns: localisations
        can be normalised or not normalised

    """

    # for each semiology, divide by the total, to get the marginal probability of that semiology i.e.
    marginal_semio_df = pd.DataFrame(columns=['Semiologies', 'numbers'])
    # assuming the index contains the list/pd.series of semiologies:
    marginal_semio_df['Semiologies'] = df.index
    marginal_semio_df['numbers'] = marginal_semio_df.sum(
        axis=1) / marginal_semio_df.sum().sum()
    marginal_semio_prob = marginal_semio_df

    # do the same for the localisations:
    marginal_loc_df = pd.DataFrame(columns=['Localisations', 'numbers'])
    marginal_loc_df['Localisations'] = df.columns
    marginal_loc_df['numbers'] = marginal_loc_df.sum(
        axis=0) / marginal_loc_df.sum().sum()
    marginal_loc_prob = marginal_loc_df

    return marginal_semio_prob, marginal_loc_prob


def p_GIFs(global_lateralisation=False,
           include_paeds_and_adults=True,
           include_only_postictals=False,
           symptom_laterality=NEUTRAL,
           dominance=NEUTRAL,
           ):
    """
    Return the normalised/unnormalised marginal probabilities for each GIF parcellation.
        for ictal semiologies only (excluding postictals)

    see marginal_GIF_probabilities() for sensitivity analyses
        e.g. by adding include_concordance=False for data queries excluding concordance
            or changing laterality or age
    """

    # normalised
    patient_all_semiology_norm = Semiology(
        ".*",
        symptoms_side=Laterality.symptom_laterality,
        dominant_hemisphere=Laterality.dominance,
        include_postictals=False,
        include_paeds_and_adults=include_paeds_and_adults,
        normalise_to_localising_values=True,
        global_lateralisation=global_lateralisation,
    )
    patient_all_semiology_norm.include_only_postictals = include_only_postictals
    all_combined_gifs_norm = patient_all_semiology_norm.get_num_datapoints_dict()
    p_GIF_norm = marginal_GIF_probabilities(all_combined_gifs_norm)

    # now not normalised version
    patient_all_semiology_notnorm = Semiology(
        ".*",
        symptoms_side=Laterality.symptom_laterality,
        dominant_hemisphere=Laterality.dominance,
        include_postictals=False,
        include_paeds_and_adults=include_paeds_and_adults=True,
        normalise_to_localising_values=False,
        global_lateralisation=global_lateralisation,
    )
    patient_all_semiology_notnorm.include_only_postictals = include_only_postictals
    all_combined_gifs_notnorm = patient_all_semiology_notnorm.get_num_datapoints_dict()
    p_GIF_notnorm = marginal_GIF_probabilities(all_combined_gifs_notnorm)

    return p_GIF_norm, p_GIF_notnorm


def p_Semiology():
    