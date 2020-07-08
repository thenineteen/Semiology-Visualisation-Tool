import numpy as np
import pandas as pd
from mega_analysis.crosstab.semiology_all_localisations import all_localisations
from mega_analysis.crosstab.hierarchy_dictionaries import postcode_dictionaries


all_locs = all_localisations()
# hierarchy_dict = postcode_dictionaries()


class Hierarchy():
    """
    To reverse the postcode system. See docstrings below.
    """

    def __init__(self, original_df):
        self.original_df = original_df.copy()
        self.new_df = original_df.copy()
        self.localisation_columns = [
            col for col in original_df.columns if col in all_locs]

    def hierarchy_reversal(self, top_level_col, low_level_cols,
                           option='max') -> pd.DataFrame:
        """
        Takes a df and returns a df

        Note that the postcode/hierarchy of localisations isn't completely invertible
        Hence, should have two options: conservative and max reversals. Default max.

        The .isin() method is so that if used on inspect_result rather than entire mega_analysis_df,
            as columns would be cleaned, it only looks for the existing columns.

        * max reversal removes all top level data if there is more granular data
            max can remove too many and give more granular localisations than original data
        * conservative reversal subtracts the max sublocalisation from the top level
        * postcode: leaves the data without hierarchy reversal

        > top_level_col: the localisation to be cleaned e.g. TL (single)
        > low_level_cols: the granular column localisations e.g. mTL as a list

        note that the order matters because self.new_df.copy() is used in all the methods:
            e.g. Hierarchy.temporal_hierarchy_reversal() method.

        """
        skip = False
        if top_level_col not in self.localisation_columns:
            # no entry for this in inspect_result df
            skip = True  # do not change the new_df

        elif option == 'max':
            self.new_df['_raw_sum'] = (
                self.new_df.loc[:, self.new_df.columns.isin(low_level_cols)]).sum(axis=1)
            condition = (self.new_df['_raw_sum'] > self.new_df[top_level_col])
            self.new_df['_reversal'] = np.where(
                condition, self.new_df[top_level_col], self.new_df['_raw_sum'])
        elif option == 'conservative':  # conservative
            self.new_df['_reversal'] = self.new_df.loc[:, self.new_df.columns.isin(
                low_level_cols)].max(axis=1)
        else:  # postcode i.e. no hierarchy reversal
            self.new_df['_reversal'] = 0

        if not skip:
            self.new_df[top_level_col] = self.new_df[top_level_col] - \
                self.new_df['_reversal']
            self.new_df.drop(labels=['_raw_sum', '_reversal'],
                             axis='columns', inplace=True, errors='ignore')

    def temporal_hierarchy_reversal(self):
        self.temporal = postcode_dictionaries(temporal=True)

        for k, v in self.temporal.items():
            self.hierarchy_reversal(
                k, v)
        self.temporal_hr = self.new_df.copy()

    def frontal_hierarchy_reversal(self):
        self.frontal = postcode_dictionaries(frontal=True)

        for k, v in self.frontal.items():
            self.hierarchy_reversal(
                k, v)
        self.frontal_hr = self.new_df.copy()

    def cingulate_hierarchy_reversal(self):
        self.cingulate = postcode_dictionaries(cingulate=True)

        for k, v in self.cingulate.items():
            self.hierarchy_reversal(
                k, v)
        self.cingulate_hr = self.new_df.copy()

    def parietal_hierarchy_reversal(self):
        self.parietal = postcode_dictionaries(parietal=True)

        for k, v in self.parietal.items():
            self.hierarchy_reversal(
                k, v)
        self.parietal_hr = self.new_df.copy()

    def occipital_hierarchy_reversal(self):
        self.occipital = postcode_dictionaries(occipital=True)

        for k, v in self.occipital.items():
            self.hierarchy_reversal(
                k, v)
        self.occipital_hr = self.new_df.copy()

    def insular_hierarchy_reversal(self):
        self.insular = postcode_dictionaries(insular=True)

        for k, v in self.insular.items():
            self.hierarchy_reversal(
                k, v)
        self.insular_hr = self.new_df.copy()

    def cerebellar_hierarchy_reversal(self):
        self.cerebellar = postcode_dictionaries(cerebellar=True)

        for k, v in self.cerebellar.items():
            self.hierarchy_reversal(
                k, v)
        self.cerebellar_hr = self.new_df.copy()

    def all_hierarchy_reversal(self):
        self.all_postcodes = postcode_dictionaries()

        for k, v in self.all_postcodes.items():
            self.hierarchy_reversal(
                k, v)
        self.all_postcodes_hr = self.new_df
