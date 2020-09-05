import mega_analysis
from mega_analysis import Semiology, Laterality
from pathlib import Path
from tqdm import tqdm
from colorama import Fore
import unittest
import sys

from mega_analysis.crosstab.file_paths import file_paths
from mega_analysis.crosstab.mega_analysis.MEGA_ANALYSIS import MEGA_ANALYSIS

file = Path(__file__).parent.parent/'resources'/'semiologies_neutral_only.txt'
list_of_terms = list(open(file, 'r'))

# list_of_terms = ['Mimetic Automatisms',
#                  'No Semiology - Only Stimulation Studies',
#                  'Non-Specific Aura', 'Olfactory-Gustatory', 'Palilalia', 'Psychic', 'Spitting', 'Vestibular', 'Vocalisation', 'Whistling']


class MultipleNeutralOnly(unittest.TestCase):
    def setUp(self):
        self.list_of_terms = list_of_terms
        print('setup')

    def list_of_terms_wrapper(self):
        for term in tqdm(self.list_of_terms, desc='Neutral Only Semiologies', bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.RED, Fore.RESET)):
            yield term

    def _test_neutral_only(self):
        self.gen_term = self.list_of_terms_wrapper()
        term = str(list(self.gen_term))
        patient = Semiology(
            term.strip(),
            symptoms_side=Laterality.LEFT,
            dominant_hemisphere=Laterality.LEFT,
        )
        heatmap = patient.get_num_datapoints_dict()
        assert isinstance(heatmap, dict)


if __name__ == '__main__':
    sys.argv.insert(1, '--verbose')
    unittest.main(argv=sys.argv)
