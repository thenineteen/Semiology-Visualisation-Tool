import pandas as pd
from mega_analysis.crosstab.gif_sheet_names import gif_sheet_names
from mega_analysis.crosstab.file_paths import file_paths


def gif_lobes_from_excel_sheets():
    """
    sort the gif parcellations as per excel gif sheet lobes.
    e.g. GIF FL = GIF Frontal Lobe - has a list of gif parcellations
    which we want to see in 3D slicer, using the GUI
    """
    _, _, excel_path, _ = file_paths()
    GIF_SHEET_NAMES = gif_sheet_names()

    lobes_mapping = {}

    for gif_lobe in GIF_SHEET_NAMES:
        gif_parcellations = pd.read_excel(
            excel_path,
            header=None, usecols="A:B",
            sheet_name=gif_lobe, engine="openpyxl",
        )
        gif_parcellations.dropna(axis=0, how='any', inplace=True)
        gif_parcellations.dropna(axis=1, how='all', inplace=True)
        gifs = gif_parcellations.astype({1: 'uint16'})
        gifs = gifs.iloc[:, 1]
        lobes_mapping[gif_lobe] = gifs.values

    return lobes_mapping
