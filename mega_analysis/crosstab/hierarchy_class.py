import numpy as np
import pandas as pd
from mega_analysis.crosstab.semiology_all_localisations import all_localisations
# from string import ascii_uppercase

# compress the locs names to the excel alphabet columns
# create aa-zz then append a-z:
all_locs = all_localisations()
# loc_iter = iter(all_locs)
# for c in ascii_uppercase:
#     double_alphabets = list(zip(c, ascii_uppercase))
# alphabets = list(ascii_uppercase).append(double_alphabets)
# alphabets_iter = iter(alphabets)
# dict_locs = dict(zip(alphabets_iter, loc_iter))


class Hierarchy():
    """
    The alphabet referrals to localisations are correct for the _dummy_data
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
        > low_level_cols: the granular column localisation e.g. mTL as a list
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
            # yield self.new_df

    def temporal_hierarchy_reversal(self):
        # STG

        self.new_df.top_level_col1 = 'TL'  # TL
        self.new_df.low_level_cols1 = ['Anterior (temporal pole)', 'Lateral Temporal',
                                       'Mesial Temporal', 'Posterior Temporal', 'Basal (including Fusiform OTMG)']
        # self.temporal_hierarchy_reversal1 =
        self.hierarchy_reversal(
            self.new_df.top_level_col1, self.new_df.low_level_cols1)

        # basal
        self.new_df.top_level_col2 = 'Basal (including Fusiform OTMG)'
        self.new_df.low_level_cols2 = ['OTMG (fusiform)']
        # self.temporal_hierarchy_reversal2 =
        self.hierarchy_reversal(
            self.new_df.top_level_col2, self.new_df.low_level_cols2)

        self.new_df.top_level_col3 = 'Mesial Temporal'  # mesial temporal
        self.new_df.low_level_cols3 = [
            'Ant Mesial Temporal', 'Post Mesial Temporal', 'Enthorinal Cortex', 'Fusiform', 'AMYGD', 'PARAHIPPOCAMPUS', 'HIPPOCAMPUS']
        # self.temporal_hierarchy_reversal3 =
        self.hierarchy_reversal(
            self.new_df.top_level_col3, self.new_df.low_level_cols3)

        self.new_df.top_level_col4 = 'Lateral Temporal'  # lateral temporal
        self.new_df.low_level_cols4 = [
            'STG (includes Transverse Temporal Gyrus, Both Planum)', 'MTG', 'ITG']
        # self.temporal_hierarchy_reversal4 =
        self.hierarchy_reversal(
            self.new_df.top_level_col4, self.new_df.low_level_cols4)

        self.new_df.top_level_col5 = 'STG (includes Transverse Temporal Gyrus, Both Planum)'
        self.new_df.low_level_cols5 = [
            'Transverse Temporal Gyrus (Heschl\'s, BA 41,  42, ?opercula)', 'Planum Temporale', 'Planum Polare']
        # self.temporal_hierarchy_reversal5 =
        self.hierarchy_reversal(
            self.new_df.top_level_col5, self.new_df.low_level_cols5)

        self.temporal_hr = self.new_df
