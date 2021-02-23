import numpy as np
import pandas as pd
from mega_analysis.crosstab.all_localisations import all_localisations

# list of all excel localisations
all_localisations = all_localisations()

# list of top level localisations we want to keep


def top_level_lobes(Bayesian=False):
    Lobes = ['TL', 'FL', 'CING', 'PL', 'OL', 'INSULA',
             'Hypothalamus', 'Sub-Callosal Cortex', 'Cerebellum', 'Perisylvian',
             'FT', 'TO', 'TP', 'FTP', 'TPO Junction',
             'PO', 'FP']
    if Bayesian:
        redistributed = ['FT', 'FTP', 'PO', 'Perisylvian', 'FP', 'Sub-Callosal Cortex', 'TO', 'TPO Junction', 'TP']
        Lobes = [i for i in Lobes if i not in redistributed]
    return Lobes


major_localisations = top_level_lobes()


# list of localisations to drop
minor_locs = [
    loc for loc in all_localisations if loc not in major_localisations]


def drop_minor_localisations(df):
    df_temp = df.drop(columns=minor_locs, inplace=False, errors='ignore')
    return df_temp
