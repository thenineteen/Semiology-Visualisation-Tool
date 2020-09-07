import pandas as pd
from pathlib import Path


def file_paths(dummy_data=False, **kwargs):
    """ Define and return paths"""
    repo_dir = Path(__file__).parent.parent.parent
    test_dir = repo_dir / 'tests'
    resources_dir = repo_dir / 'resources'

    if dummy_data:
        Database_path = test_dir / '_dummy_data.csv'
        SemioDict_path = test_dir / '_dummy_semiology_dictionary.yaml'
        mappings_folder = test_dir / 'test_mappings'
    elif "Beta" in kwargs:
        Database_path = resources_dir / 'syst_review_single_table.xlsx'
        SemioDict_path = resources_dir / 'semiology_dictionary.yaml'
        mappings_folder = resources_dir / 'mappings'
    else:
        Database_path = resources_dir / 'Semio2Brain Database.xlsx'
        SemioDict_path = resources_dir / 'semiology_dictionary.yaml'
        mappings_folder = resources_dir / 'mappings'

    return repo_dir, resources_dir, Database_path, SemioDict_path, mappings_folder
