from enum import Enum
from pathlib import Path
from typing import Optional, List, Dict

import yaml
import numpy as np
import pandas as pd

from mega_analysis.crosstab.mega_analysis.MEGA_ANALYSIS import MEGA_ANALYSIS
from mega_analysis.crosstab.mega_analysis.QUERY_SEMIOLOGY import QUERY_SEMIOLOGY
from mega_analysis.crosstab.mega_analysis.QUERY_LATERALISATION import QUERY_LATERALISATION
from mega_analysis.crosstab.mega_analysis.exclusions import (
    exclusions,
    exclude_ET,
    exclude_sEEG,
    exclude_cortical_stimulation,
    exclude_seizure_free,
)


# Define paths
repo_dir = Path(__file__).parent.parent
resources_dir = repo_dir / 'resources'
excel_path = resources_dir / 'syst_review_single_table.xlsx'
semiology_dict_path = resources_dir / 'semiology_dictionary.yaml'


# Read Excel file only three times at initialisation
mega_analysis_df, _, _ = MEGA_ANALYSIS(excel_data=excel_path)
map_df_dict = pd.read_excel(
    excel_path,
    header=1,
    sheet_name=['GIF TL', 'GIF FL', 'GIF PL', 'GIF OL', 'GIF CING', 'GIF INSULA', 'GIF CEREBELLUM']
)
gif_lat_file = pd.read_excel(
    excel_path,
    header=0,
    sheet_name='Full GIF Map for Review '
)

def recursive_items(dictionary):
    """https://stackoverflow.com/a/39234154/3956024"""
    for key, value in dictionary.items():
        if type(value) is dict:
            yield from recursive_items(value)
        else:
            yield key


def get_all_semiology_terms():
    with open(semiology_dict_path) as f:
        dictionary = yaml.load(f, Loader=yaml.FullLoader)
    return sorted(recursive_items(dictionary))

# Read YAML
all_semiology_terms = get_all_semiology_terms()

# Define constants
class Laterality(Enum):
    LEFT = 'L'
    RIGHT = 'R'
    NEUTRAL = None


class Semiology:
    def __init__(
            self,
            term: str,
            symptoms_side: Laterality,
            dominant_hemisphere: Laterality,
            include_seizure_freedom: bool = True,
            include_concordance: bool = True,
            include_seeg: bool = True,
            include_cortical_stimulation: bool = True,
            include_et_topology_ez: bool = True,
            ):
        self.term = term
        self.symptoms_side = symptoms_side
        self.dominant_hemisphere = dominant_hemisphere
        self.data_frame = self.remove_exclusions(
            mega_analysis_df,
            include_seizure_freedom,
            include_concordance,
            include_seeg,
            include_cortical_stimulation,
            include_et_topology_ez,
        )

    @staticmethod
    def remove_exclusions(
            df: pd.DataFrame,
            include_seizure_freedom: bool,
            include_concordance: bool,
            include_seeg: bool,
            include_cortical_stimulation: bool,
            include_et_topology_ez: bool,
            ) -> pd.DataFrame:
        if not include_concordance:
            df = exclusions(df, CONCORDANCE=True)
        if not include_seizure_freedom:
            df = exclude_seizure_free(df)
        if not include_et_topology_ez:
            df = exclude_ET(df)
        if not include_seeg:
            df = exclude_sEEG(df)
        if not include_cortical_stimulation:
            df = exclude_cortical_stimulation(df)
        return df

    def query_semiology(self) -> pd.DataFrame:
        if self.term in all_semiology_terms:
            path = semiology_dict_path
        else:
            path = None
        inspect_result = QUERY_SEMIOLOGY(
            self.data_frame,
            semiology_term=self.term,
            semiology_dict_path=path,
        )
        return inspect_result

    def query_lateralisation(self) -> Optional[pd.DataFrame]:
        query_semiology_result = self.query_semiology()
        all_combined_gifs = QUERY_LATERALISATION(
            query_semiology_result,
            self.data_frame,
            map_df_dict,
            gif_lat_file,
            side_of_symptoms_signs=self.symptoms_side.value,
            pts_dominant_hemisphere_R_or_L=self.dominant_hemisphere.value,
        )
        return all_combined_gifs

    def get_num_patients_dict(self) -> Optional[dict]:
        query_lateralisation_result = self.query_lateralisation()
        if query_lateralisation_result is None:
            num_patients_dict = None
        else:
            array = np.array(query_lateralisation_result)
            _, labels, patients = array.T
            num_patients_dict = {
                int(label): float(num_patients)
                for (label, num_patients)
                in zip(labels, patients)
            }
        return num_patients_dict
