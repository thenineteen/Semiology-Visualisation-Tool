import unittest
from mega_analysis.semiology import Semiology, Laterality


class TestSemiology(unittest.TestCase):
    def test_existing_aphasia(self):
        semiology = Semiology('Aphasia', Laterality.LEFT, Laterality.LEFT)
        num_patients_dict = semiology.get_num_patients_dict()
        self.assertIs(type(num_patients_dict), dict)

    def test_neutral_symptoms_side_aphasia(self):
        semiology = Semiology('Aphasia', Laterality.NEUTRAL, Laterality.LEFT)
        num_patients_dict = semiology.get_num_patients_dict()
        self.assertIs(type(num_patients_dict), dict)

    def test_neutral_dominant_hemisphere_aphasia(self):
        semiology = Semiology('Aphasia', Laterality.LEFT, Laterality.NEUTRAL)
        num_patients_dict = semiology.get_num_patients_dict()
        self.assertIs(type(num_patients_dict), dict)

    def test_neutral_all_aphasia(self):
        semiology = Semiology(
            'Aphasia', Laterality.NEUTRAL, Laterality.NEUTRAL)
        num_patients_dict = semiology.get_num_patients_dict()
        self.assertIs(type(num_patients_dict), dict)


    def test_existing_aphemia(self):
        semiology = Semiology('Aphemia', Laterality.LEFT, Laterality.LEFT)
        num_patients_dict = semiology.get_num_patients_dict()
        self.assertIs(type(num_patients_dict), dict)

    def test_neutral_symptoms_side_aphemia(self):
        semiology = Semiology('Aphemia', Laterality.NEUTRAL, Laterality.LEFT)
        num_patients_dict = semiology.get_num_patients_dict()
        self.assertIs(type(num_patients_dict), dict)

    def test_neutral_dominant_hemisphere_aphemia(self):
        semiology = Semiology('Aphemia', Laterality.LEFT, Laterality.NEUTRAL)
        num_patients_dict = semiology.get_num_patients_dict()
        self.assertIs(type(num_patients_dict), dict)

    def test_neutral_all_aphemia(self):
        semiology = Semiology(
            'Aphemia', Laterality.NEUTRAL, Laterality.NEUTRAL)
        num_patients_dict = semiology.get_num_patients_dict()
        self.assertIs(type(num_patients_dict), dict)


    def test_existing_blink(self):
        semiology = Semiology('Blink', Laterality.LEFT, Laterality.LEFT)
        num_patients_dict = semiology.get_num_patients_dict()
        self.assertIs(type(num_patients_dict), dict)

    def test_neutral_symptoms_side_blink(self):
        semiology = Semiology('Blink', Laterality.NEUTRAL, Laterality.LEFT)
        num_patients_dict = semiology.get_num_patients_dict()
        self.assertIs(type(num_patients_dict), dict)

    def test_neutral_dominant_hemisphere_blink(self):
        semiology = Semiology('Blink', Laterality.LEFT, Laterality.NEUTRAL)
        num_patients_dict = semiology.get_num_patients_dict()
        self.assertIs(type(num_patients_dict), dict)

    def test_neutral_all_blink(self):
        semiology = Semiology(
            'Blink', Laterality.NEUTRAL, Laterality.NEUTRAL)
        num_patients_dict = semiology.get_num_patients_dict()
        self.assertIs(type(num_patients_dict), dict)


    def test_non_existing(self):
        semiology = Semiology('No semiology', Laterality.LEFT, Laterality.LEFT)
        num_patients_dict = semiology.get_num_patients_dict()
        self.assertIs(num_patients_dict, None)
