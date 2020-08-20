import pandas as pd
import numpy as np
from pathlib import Path

# Define paths
repo_dir = Path(__file__).parent.parent.parent.parent
resources_dir = repo_dir / 'resources'
excel_path = resources_dir / 'Semio2Brain Database_Mappings_Calibration.xlsx'


def gifs_lat_factor(*gif_lat_file):
    """
    factor function. opens the right/left gif parcellations from excel and extracts the right/left gifs as series/list.
    """
    if not gif_lat_file:
        gif_lat_file = pd.read_excel(
            excel_path,
            header=0,
            sheet_name='Full GIF Map for Review '
        )
    gifs_right = gif_lat_file.loc[gif_lat_file['R'].notnull(), 'R'].copy()
    gifs_left = gif_lat_file.loc[gif_lat_file['L'].notnull(), 'L'].copy()

    return gifs_right, gifs_left
