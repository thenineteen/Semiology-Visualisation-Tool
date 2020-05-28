import unittest
from mega_analysis.semiology import gif_lobes_from_excel_sheets


class TestQuerySemiology(unittest.TestCase):
    def test_is_dict(self):
        self.assertIsInstance(gif_lobes_from_excel_sheets(), dict)
