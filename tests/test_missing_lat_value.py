import unittest
import sys

from mega_analysis.semiology import mega_analysis_df


class Missing_Lat_Values(unittest.TestCase):
    def setUp(self):
        self.df = mega_analysis_df.copy()

    def test_missing_CL_IL_BL_DomH_NonDomH(self):
        """
        A Semio2Brain Database test to ensure any rows with lateralising values have entries for CL or IL or BL or DomH or NonDomH.
        Output writes CSV file to resources with list of References with entries to be corrected.

        # """
        # sub_lats = ['IL', 'CL', 'DomH', 'NonDomH',
        #             #'BL (Non-lateralising)',
        #             ]
        # # min_count of 1 makes empty sum to be nan.
        # self.df['Lat_Values'] = self.df[sub_lats].sum(
        #     axis=1, skipna=True, min_count=0)

        # mask_Lateralising = self.df['Lateralising'].notnull()
        # # now, all notnull lateralising must also have notnull Lat_Values:
        # test1 = self.df.loc[mask_Lateralising, 'Lat_Values']
        # mistake = test1.isnull().any()

        # if mistake:
        #     number_missing_rows_values = test1.isnull().sum()
        #     i = test1.isnull().index
        #     sub_lats.insert(0, 'Reference')
        #     sub_lats.insert(1, 'Lateralising')
        #     k = self.df.loc[i, sub_lats]

        #     print('\n\nTest1: Number of missing row values = ',
        #           number_missing_rows_values)
        #     print('\n\n', i)
        #     k.groupby(by='Reference').sum().to_csv(
        #         r'C:\Users\ali_m\AnacondaProjects\PhD\Semiology-Visualisation-Tool\resources\Database_test_missing_lat_output\test1_generated_missing_lat_values.csv')

        # assert not mistake

    def test_UnequalSum_CL_IL_BL_DomH_NonDomH(self):
        """
        Sum the values, except for the BL cases, and ensure match the 'Lateralising' column.
        """
        sub_lats = ['IL', 'CL', 'DomH', 'NonDomH']
        self.df['Lat_Values'] = self.df[sub_lats].sum(
            axis=1, skipna=True, min_count=1)

        self.df = self.df.astype({'Lateralising': 'int32',
                                  'Lat_Values': 'int32'},
                                 errors='ignore')
        test2 = (self.df['Lateralising'].notnull()
                 == self.df['Lat_Values'].notnull())

        if not test2.all():
            i = (test2 == False)
            unmatched_sums = i.sum()
            sub_lats.insert(0, 'Reference')
            sub_lats.insert(1, 'Lateralising')
            k = self.df.loc[i, sub_lats]

            print('\n\nTest2: Number of sums not matching = ',
                  unmatched_sums)
            # k.groupby(by='Reference').sum().to_csv(
            #     r'C:\Users\ali_m\AnacondaProjects\PhD\Semiology-Visualisation-Tool\resources\Database_test_missing_lat_output\test2_generated_UnmatchedSum_values.csv')

        assert test2.all()


if __name__ == '__main__':
    sys.argv.insert(1, '--verbose')
    unittest.main(argv=sys.argv)
s
