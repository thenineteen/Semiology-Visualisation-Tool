import unittest
from mega_analysis.crosstab.gif_lobes_from_excel_sheets import gif_lobes_from_excel_sheets


class TestQuerySemiology(unittest.TestCase):
    def test_is_dict(self):
        a = self.assertIsInstance(gif_lobes_from_excel_sheets(), dict)
        print(a)

test = TestQuerySemiology()
test.test_is_dict()
