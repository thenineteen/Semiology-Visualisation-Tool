import pandas as pd


def gif_sheet_names():
    """
    Update this if the sheet names change or more are added.
    Used by semiology.py and gif_lobed_from_excel_sheets.py
    """

    gif_sheet_names = [
        'GIF TL', 'GIF FL', 'GIF PL', 'GIF OL',
        'GIF CING', 'GIF INSULA',
        'GIF HYPOTHALAMUS', 'GIF CEREBELLUM', 'GIF MIXED',
    ]

    return gif_sheet_names
