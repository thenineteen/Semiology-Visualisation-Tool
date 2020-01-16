import pandas as pd

def all_localisations(file="C:\\Downloads\\4. SystReview Single Table (NEW CROSSTAB) 25 July_ last.xlsx",
                      localisation_columns="R:CN"):
    """
    Import the excel spreadsheet of 1,171 journal paper reviews and return a list of the anatomical brain region terms. 
    Used as default when importing the spreadsheet in semiology_lateralisation_localisation.

    """
# import the columns containing the localisation terms
    all_localisations = pd.read_excel(file, nrows=0, usecols=localisation_columns, header=0)

# turn into a list
    all_localisations_list = list(all_localisations)

# filter the empty cells
    all_localisations_list_filtered = [item for item in all_localisations_list if "Unnamed" not in item]

    return all_localisations_list_filtered