import pandas as pd
from pathlib import Path

def file_paths():
    # Define paths
    repo_dir = Path(__file__).parent.parent
    resources_dir = repo_dir / 'resources'
    excel_path = resources_dir / 'syst_review_single_table.xlsx'
    semiology_dict_path = resources_dir / 'semiology_dictionary.yaml'

    return repo_dir, resources_dir, excel_path, semiology_dict_path