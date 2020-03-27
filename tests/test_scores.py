import unittest
from mega_analysis import get_scores_dict

class TestScores(unittest.TestCase):
    def test_scores_dict(self):
        scores_dict = get_scores_dict(catch_errors=False)
