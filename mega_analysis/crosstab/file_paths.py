import pandas as pd
from pathlib import Path

def file_paths(dummy_data=False):
    # Define paths
    repo_dir = Path(__file__).parent.parent.parent
    resources_dir = repo_dir / 'resources'
    test_dir = repo_dir / 'tests'
    if dummy_data:
        excel_path = test_dir / '_dummy_data.xlsx'
        semiology_dict_path = test_dir / '_dummy_semiology_dictionary.yaml'
    else:
        excel_path = resources_dir / 'syst_review_single_table.xlsx'
        semiology_dict_path = resources_dir / 'semiology_dictionary.yaml'

    return repo_dir, resources_dir, excel_path, semiology_dict_path