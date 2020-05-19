import pandas as pd
from mega_analysis.crosstab.mega_analysis
from resources.gif_sheet_names import gif_sheet_names

def gif_lobes_from_excel_sheets():
    """
    sort the gif parcellations as per excel gif sheet lobes.
    e.g. GIF FL = GIF Frontal Lobe - has a list of gif parcellations
    which we want to see in 3D slicer, using the GUI
    """
    gif_sheet_names = gif_sheet_names()

    lobes_mapping = {}

    for gif_lobe in gif_sheet_names:
        gif_parcellations = pd.read_excel(
            excel_path,
            header=None, index_col="A,B",
            sheet_name=gif_lobe
        )

        lobes_mapping[gif_lobe] = gif_parcellations["B"]

    return lobes_mapping

