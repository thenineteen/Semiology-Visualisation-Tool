import pandas as pd

def mapping(excel_file = "D:\\Ali USB Backup\\1 PhD\\4. SystReview Single Table (NEW CROSSTAB) 25 July_ last.xlsx"):
    """
    Uses Ali and Gloria's brain reported localisation in literature to GIF parcellations,
    using their mapping.
    
    # These are the maps for each lobe
    #     mapping_FL = map_df_dict['GIF FL']
    #     mapping_TL = map_df_dict['GIF TL']
    #     mapping_PL = map_df_dict['GIF PL']
    #     mapping_OL = map_df_dict['GIF OL']
    #     mapping_CING = map_df_dict['GIF CING']
    #     mapping_INSULA = map_df_dict['GIF INSULA']
    
    GIF parcellation missing hypothalamic parcellation?
    
    Aug 2019 Ali Alim-Marvasti
    
    """
    map_df_dict = pd.read_excel(excel_file, 
#                            nrows=n_rows, 
#                            usecols=usecols, 
                           header=1, 
#                            index=index,
                           sheet_name=['GIF TL', 'GIF FL', 'GIF PL', 'GIF OL', 'GIF CING', 'GIF INSULA']
                          )
    
    for lobe in map_df_dict.keys():
        map_df_dict[lobe] = map_df_dict[lobe].dropna(axis='rows', how='all')
        map_df_dict[lobe] = map_df_dict[lobe].dropna(axis='columns', how='all')
        


    return map_df_dict


def big_map():
    """
    Appends all the localisation to gif mapping DataFrames into one big DataFrame.
    """

    map_df_dict = mapping()


    one_map = pd.DataFrame()
    for lobe in map_df_dict.keys():
        one_map = one_map.append(map_df_dict[lobe], sort=False)
        
    return one_map


def pivot_result_to_one_map(pivot_result, one_map):
    """
    2. for each col in pivot_result, find the mapping col numbers, dropna axis rows.
    3. then make new col and add the ~pt numbers and pixel intensity for all i.e. ffill-like using slicing

    Makes a dataframe as it goes along appending all the mappings.
    """
    
    # checks
    if (len([col for col in pivot_result if col not in one_map]))>0:
        print(len([col for col in pivot_result if col not in one_map]), 'localisation column(s) in the pivot_result which cannot be found in one_map')
        print([col for col in pivot_result if col not in one_map])
    else:
        print('No issues: pivot_result compared to one_map and all localisations are ready for analysis.')
    
    # initialisations
    individual_cols = [col for col in pivot_result if col in one_map]
    all_gifs = pd.DataFrame()
    
    # populate the return df
    for col in individual_cols:
        col_gifs = one_map[[col]].dropna(axis='rows', how='all')
        # add the ~pts numbers:
        col_gifs.loc[:, 'pt #s'] = int(pivot_result[col].values)
        all_gifs = all_gifs.append(col_gifs, sort=False)

    # stack the resulting all_gifs (values are in 3rd column)
    all_gifs = all_gifs.melt(var_name='localisation', value_name='gif parcellations')  # df
    all_gifs = all_gifs.dropna(axis='rows', how='any')  # required as melted
#     all_gifs = all_gifs.stack()  #  gives a series

    # insert a new first col which contains the index value of pivot_result (i.e. the semiology term)
    # this is for Rachel Sparks's requirement:
    all_gifs.insert(0, 'Semiology Term', np.nan)
    all_gifs.loc[0, 'Semiology Term'] = str(list(pivot_result.index.values))
    
    return all_gifs
