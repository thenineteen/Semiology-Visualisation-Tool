from pathlib import Path
from tqdm import tqdm
from colorama import Fore
from collections import Counter
import pandas as pd

from mega_analysis.crosstab.file_paths import file_paths
from mega_analysis.crosstab.mega_analysis.MEGA_ANALYSIS import MEGA_ANALYSIS
from mega_analysis import Semiology, Laterality

file = Path(__file__).parent/'resources'/'semiologies_neutral_only.txt'
file2 = Path(__file__).parent/'resources'/'semiologies_neutral_also.txt'
file3 = Path(__file__).parent/'resources'/'semiologies_neutral_also.txt'
list_of_terms = list(open(file, 'r'))
list_of_terms2 = list(open(file2, 'r'))
list_of_terms3 = list(open(file3, 'r'))
semiologies = list_of_terms + list_of_terms2 + list_of_terms3


 # initialise
num_datapoints_dict = {}
p_GIF_given_S = pd.DataFrame()


for term in tqdm(semiologies, desc='Semiologies', bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.RED, Fore.RESET)):
    if term.strip() in ["No Semiology - Only Stimulation Studies", "Hypomotor"]:
        continue
    patient = Semiology(
        term.strip(),
        symptoms_side=Laterality.NEUTRAL,
        dominant_hemisphere=Laterality.NEUTRAL,
        granular=True,  # hierarchy reversal
        include_cortical_stimulation=False,
        include_et_topology_ez=False,
        include_spontaneous_semiology=True,  # SS
        normalise_to_localising_values=True,  # normalise to pt numbers
        include_paeds_and_adults=True,  # paeds and adults
    )


    num_datapoints_dict[term.strip()], all_combined_gif_df = patient.get_num_datapoints_dict()


# set the zero ones:
num_datapoints_dict['Hypomotor'] = num_datapoints_dict['Epigastric']
for k, v in num_datapoints_dict['Hypomotor'].items():
    num_datapoints_dict['Hypomotor'][k] = 0
print('done')

