import pandas as pd
import numpy as np


def INVERSE_LOCALISING_VALUES(df):
    """
    Alter the DataFrame to allocate inverse localising values based on spread of localisations.
    The more widepsread a region a single patient's EZ/SOZ localises to, the lower its localising-value.

    As per call in semiology.py, this option is only utilised if granular/hierarchy-reversal is True.

    Alim-Marvasti Sept 2020.
    """

    return df
