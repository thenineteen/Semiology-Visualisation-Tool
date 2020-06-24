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

    def temporal_hierarchy_reversal(self):
        self.new_df.top_level_col1 = 'TL'  # TL
        self.new_df.low_level_cols1 = ['Anterior (temporal pole)', 'Lateral Temporal',
                                       'Mesial Temporal', 'Posterior Temporal', 'Basal (including Fusiform OTMG)']
        self.hierarchy_reversal(
            self.new_df.top_level_col1, self.new_df.low_level_cols1)

        self.new_df.top_level_col2 = 'Basal (including Fusiform OTMG)'
        self.new_df.low_level_cols2 = ['OTMG (fusiform)']
        self.hierarchy_reversal(
            self.new_df.top_level_col2, self.new_df.low_level_cols2)

        self.new_df.top_level_col3 = 'Mesial Temporal'  # mesial temporal
        self.new_df.low_level_cols3 = [
            'Ant Mesial Temporal', 'Post Mesial Temporal', 'Enthorinal Cortex', 'Fusiform', 'AMYGD', 'PARAHIPPOCAMPUS', 'HIPPOCAMPUS']
        self.hierarchy_reversal(
            self.new_df.top_level_col3, self.new_df.low_level_cols3)

        self.new_df.top_level_col4 = 'Lateral Temporal'  # lateral temporal
        self.new_df.low_level_cols4 = [
            'STG (includes Transverse Temporal Gyrus, Both Planum)', 'MTG', 'ITG']
        self.hierarchy_reversal(
            self.new_df.top_level_col4, self.new_df.low_level_cols4)

        self.new_df.top_level_col5 = 'STG (includes Transverse Temporal Gyrus, Both Planum)'
        self.new_df.low_level_cols5 = [
            'Transverse Temporal Gyrus (Heschl\'s, BA 41,  42, ?opercula)', 'Planum Temporale', 'Planum Polare']
        self.hierarchy_reversal(
            self.new_df.top_level_col5, self.new_df.low_level_cols5)

        self.temporal_hr = self.new_df

    # def frontal_hierarchy_reversal(self):
    #     self.new_df.top_level_col = 'FL'
    #     self.new_df.low_level_cols = []
    #     self.hierarchy_reversal(
    #         self.new_df.top_level_col, self.new_df.low_level_cols)

    def frontal_hierarchy_reversal(self):
        self.frontal = {
            'FL': [
                'frontal pole',
                'Pre-frontal (BA 8, 9, 10, 11, 12, 13, 14, 24, 25, 32, 44, 45, 46, 47)',
                'Medial Frontal\n(should include medial premotor and its constituents as its subsets)',
                'Primary Motor Cortex (Pre-central gyrus, BA 4, Rolandic)',
                'SFG (F1)',
                'MFG (F2)',
                'IFG (F3)\n(BA 44,45,47)',
                'Premotor frontal (posterior frontal)',
                'SMA (pre-central gyrus; posterior SFG, MFG)',
                'SSMA',
            ],
            'Pre-frontal (BA 8, 9, 10, 11, 12, 13, 14, 24, 25, 32, 44, 45, 46, 47)': [
                'DL-PFC\n(BA 46)\n(include subgroups BA 9, 8, 10 - frontopolar/anterior prefrontal)',
                'gyrus rectus (basal = gyrus rectus and OFC)',
                'Orbito-frontal (BA 10, 11, 12/47) (basal = gyrus rectus and OFC)',
            ],
            'Primary Motor Cortex (Pre-central gyrus, BA 4, Rolandic)': [
                'medial precentral',
                'Rolandic Operculum (low BA4)',
            ],
            'SFG (F1)': [
                'Med SFG',
                'Ant SFG',
            ],
            'MFG (F2)': [
                'Ant MFG',
            ],
            'IFG (F3)\n(BA 44,45,47)': [
                'Pars orbitalis (subgroup of IFG)\n(BA 47)',
                'Pars Triangularis (subgroup IFG)',
                'Pars opercularis (BA 44)(subgroup IFG, ?opercula)',
            ],
            'Premotor frontal (posterior frontal)': [
                'Ant Premotor\n(BA 8, frontal-eye-fields)',
                'Lateral Premotor\n(BA 6)',
                'Medial Premotor (including pre SMA)',
            ],
            'Orbito-frontal (BA 10, 11, 12/47) (basal = gyrus rectus and OFC)': [
                'Ant OF',
                'Post OF',
                'Lat OF',
                'Med OF',
            ],
            'Lateral Premotor\n(BA 6)': [
                'Ventro-lateral premotor',
                'Dorso-lateral premotor',
            ]
        }

        for k, v in self.frontal.items():
            self.hierarchy_reversal(
                k, v)
        self.frontal_hr = self.new_df
