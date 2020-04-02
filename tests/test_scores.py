import unittest
from mega_analysis.scores import Semiology

class TestScores(unittest.TestCase):
    def test_existing_aphasia(self):
        semiology = Semiology('Aphasia', left=True)
        num_patients_dict = semiology.get_num_patients_dict()
        self.assertIs(type(num_patients_dict), dict)

    def test_existing_aphemia(self):
        semiology = Semiology('Aphemia', left=True)
        num_patients_dict = semiology.get_num_patients_dict()
        self.assertIs(type(num_patients_dict), dict)
