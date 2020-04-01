import unittest
from mega_analysis import get_scores_dict

class TestScores(unittest.TestCase):
    def test_existing_aphasia(self):
        scores_dict = get_scores_dict('Aphasia', catch_errors=False)
        self.assertIs(type(scores_dict), dict)

    def test_existing_aphemia(self):
        scores_dict = get_scores_dict('Aphemia', catch_errors=False)
        self.assertIs(type(scores_dict), dict)
