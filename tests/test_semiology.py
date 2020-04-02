import unittest
from mega_analysis.semiology import Semiology

class TestSemiology(unittest.TestCase):
    def test_existing_aphasia(self):
        semiology = Semiology('Aphasia', left=True)
        num_patients_dict = semiology.get_num_patients_dict()
        self.assertIs(type(num_patients_dict), dict)

    def test_existing_aphemia(self):
        semiology = Semiology('Aphemia', left=True)
        num_patients_dict = semiology.get_num_patients_dict()
        self.assertIs(type(num_patients_dict), dict)

    def test_non_existing(self):
        semiology = Semiology('Not a semiology', left=True)
        num_patients_dict = semiology.get_num_patients_dict()
        self.assertIs(num_patients_dict, None)
