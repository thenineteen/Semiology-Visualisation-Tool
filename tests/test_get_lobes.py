import unittest

from mega_analysis.crosstab.gif_lobes_from_excel_sheets import \
    gif_lobes_from_excel_sheets
from mega_analysis.crosstab.semiology_all_localisations import \
    all_localisations
from mega_analysis.crosstab.semiology_lateralisation_localisation import \
    semiology_lateralisation_localisation


class LocalisationLobesAndHierarchies(unittest.TestCase):
    def test_lobes_is_dict(self):
        self.assertIsInstance(gif_lobes_from_excel_sheets(), dict)

    def test_localisation_compatibility(self):
        """
        Test the melted df_localisation has localisation terms which are ALL found in list all_localisations()
        """
        all_localisations_list_filtered = all_localisations()
        df_localisation_melt = semiology_lateralisation_localisation()

        mask = df_localisation_melt['Localisation'].isin(
            all_localisations_list_filtered)
        assert mask.all() == True
