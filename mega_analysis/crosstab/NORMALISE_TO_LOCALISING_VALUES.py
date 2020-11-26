import pandas as pd
import numpy as np
from mega_analysis.crosstab.all_localisations import all_localisations


def NORMALISE_TO_LOCALISING_VALUES(inspect_result, type='all'):
    """
    Alter the DataFrame to normalise values to localising column value: i.e. conservation of localising semiology datapoints.
    based on spread of localisations.
    The more regions a semiology EZ/SOZ localises to, the lower its brain localising-value.
    Makes localisiing semiology the unit of analysis and when using type='all', also imputes possible missing data based
        on localisations (brain regions) present.
    See also tooltip in SVT for this option (SemiologyVisualisation module).

    As per call in semiology.py, this option is only utilised if granular/hierarchy-reversal is True
        OR if the low resolution option is selected (top_level_lobes_only).

    Also useful for Sankey diagram: preservation of 'Localising' flows.
        e.g. 1 localising value for epigastric localises to hippocampus (1) and amygdala (1) and Insula (1).
        With NLV, each of hippo, amygdala and insular values changes to 0.33 (1/3rd).
        This can create artefactually lower numbers for wide intralobar spreads (amygdala and hippo), but useful for conservation of localising value.

    Alim-Marvasti Sept 2020.
    """

    new_inspect_result = inspect_result.copy()

    # get all loc columns
    all_locs = all_localisations()
    locs = [i for i in new_inspect_result.columns if i in all_locs]

    # set index

    # Find semiology row's Localising sum and then divide by the sum of localising regions (e.g. FL and TL)
    # new_inspect_result.loc[:, 'ratio'] = np.nan
    new_inspect_result.loc[:, 'ratio'] = new_inspect_result['Localising'] / \
        new_inspect_result[locs].sum(axis=1)
    new_inspect_result = new_inspect_result.astype({'ratio': 'float'})

    # only change if ratio <1
    if type == 'ratio<1':
        gif_indices = (new_inspect_result['ratio'] < 1)
        if gif_indices.any():
            # df.multiply (not series.multiply). ratio is series. axis=0 otherwise deafult is columns.
            inspect_result.loc[gif_indices, locs] = \
                (new_inspect_result.loc[gif_indices, locs]).multiply(
                    new_inspect_result.loc[gif_indices, 'ratio'],
                    axis=0,
            )
    else:
        inspect_result.loc[:, locs] = \
            (new_inspect_result.loc[:, locs]).multiply(
                new_inspect_result.loc[:, 'ratio'], axis=0)

    # new_inspect_result.drop(columns='ratio', inplace=True)
    return inspect_result
