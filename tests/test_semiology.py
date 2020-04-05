import unittest
from mega_analysis.semiology import (
    Semiology,
    Laterality,
    get_df_from_dicts,
    normalise_semiologies_df,
    combine_semiologies_df,
)


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


    def test_existing_head_version(self):
        semiology = Semiology('Head version', Laterality.LEFT, Laterality.LEFT)
        num_patients_dict = semiology.get_num_patients_dict()
        self.assertIs(type(num_patients_dict), dict)

    def test_neutral_symptoms_side_head_version(self):
        semiology = Semiology('Head version', Laterality.NEUTRAL, Laterality.LEFT)
        num_patients_dict = semiology.get_num_patients_dict()
        self.assertIs(type(num_patients_dict), dict)

    def test_neutral_dominant_hemisphere_head_version(self):
        semiology = Semiology('Head version', Laterality.LEFT, Laterality.NEUTRAL)
        num_patients_dict = semiology.get_num_patients_dict()
        self.assertIs(type(num_patients_dict), dict)

    def test_neutral_all_head_version(self):
        semiology = Semiology(
            'Head version', Laterality.NEUTRAL, Laterality.NEUTRAL)
        num_patients_dict = semiology.get_num_patients_dict()
        self.assertIs(type(num_patients_dict), dict)


    def test_non_existing(self):
        semiology = Semiology('No semiology', Laterality.LEFT, Laterality.LEFT)
        num_patients_dict = semiology.get_num_patients_dict()
        self.assertIs(num_patients_dict, None)


    def test_combine_semiologies(self):
        semiologies_dicts = {
            1: dict(x=0, y=1, z=1000),
            2: dict(x=1, y=2, z=3),
            3: dict(x=50, y=50, z=5),
            4: dict(x=0, y=12, z=15),
            5: dict(x=0, y=0, z=0),
        }
        df = get_df_from_dicts(semiologies_dicts)
        normalised = normalise_semiologies_df(df)
        combined = combine_semiologies_df(normalised)
        self.assertAlmostEqual(combined['x'], 100/3)
        self.assertAlmostEqual(combined['y'], 76.7)
        self.assertAlmostEqual(combined['z'], 100)

    def test_combine_single_semiology(self):
        semiologies_dicts = {
            2: dict(x=1, y=2, z=3),
        }
        df = get_df_from_dicts(semiologies_dicts)
        normalised = normalise_semiologies_df(df)
        combined = combine_semiologies_df(normalised)
        self.assertAlmostEqual(combined['x'], 0)
        self.assertAlmostEqual(combined['y'], 50)
        self.assertAlmostEqual(combined['z'], 100)
