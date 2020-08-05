import pandas as pd
from pathlib import Path


def all_localisations(excel_columns="R:DP"):
    """
    Import the excel spreadsheet of 312 included journal paper reviews (4649 patients) and
    return a list of the anatomical brain region terms.
    Used as default when importing the spreadsheet in semiology_lateralisation_localisation.
    """
# set the path to excel file:
    repo_dir = Path(__file__).parent.parent.parent
    resources_dir = repo_dir / 'resources'
    excel_path = resources_dir / 'Semio2Brain Database.xlsx'

# import the columns containing the localisation terms
    df_all_localisations = pd.read_excel(
        excel_path, nrows=0, usecols=excel_columns, header=1)

# turn into a list
    all_localisations_list = list(df_all_localisations)

# filter the empty cells
    all_localisations_list_filtered = [
        item for item in all_localisations_list if "Unnamed" not in item]

    return all_localisations_list_filtered


if __name__ == '__main__':
    all_localisations_list_filtered = all_localisations()
