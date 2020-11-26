import numpy as np
import pandas as pd
from mega_analysis.crosstab.all_localisations import all_localisations
from mega_analysis.Sankey_Functions import top_level_lobes

# list of all excel localisations
all_localisations = all_localisations()

# list of top level localisations we want to keep
major_localisations = top_level_lobes()

# list of localisations to drop
minor_locs = [
    loc for loc in all_localisations if loc not in major_localisations]


def drop_minor_localisations(df):
    df_temp = df.drop(columns=minor_locs, inplace=False)
    return df_temp
