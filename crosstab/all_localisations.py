import pandas as pd

def all_localisations(file="C:\\Users\\ali_m\\Downloads\\Marvasti crosstab (2).xlsx",
                      localisation_columns="R:CG"):
    
# import the columns containing the localisation terms
    all_localisations = pd.read_excel(file, nrows=0, usecols=localisation_columns, header=0)

# turn into a list
    all_localisations_list = list(all_localisations)

# filter the empty cells
    all_localisations_list_filtered = [item for item in all_localisations_list if "Unnamed" not in item]

    return all_localisations_list_filtered