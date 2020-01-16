from .QUERY_SEMIOLOGY import *
import numpy as np
import pandas as pd

def QUERY_INTERSECTION_TERMS(df, *args):
    """
    Runs two QUERY_SEMIOLOGY searches, returns the intersection of both queries.
    Can be used to find pts with semiology involving e.g. "head" and "sensation".

    In disctinction to QUERY_SEMIOLOGY where a list can be given and searched as "OR",
    here, variable number of args can be given s tuple and treated as "AND".

    Alim-Marvasti Aug 2019

    Note: at some point the exclusions.py can be refactored using this function.
    """
    n = 0
    for arg in args:
        n += 1
        query_inspection = QUERY_SEMIOLOGY(df, semiology_term=arg,
                                            ignore_case=True, use_semiology_dictionary=False,
                                            # col1=col1, col2=col1
                                            )

        # can't merge the first df
        if n==1:
            inspect_combined_result = query_inspection
            continue

        # ans is df of the intersection of the above two, keep the index otherwise it is reset
        inspect_combined_result = query_inspection.reset_index().merge(inspect_combined_result, how="inner").set_index('index')
        if inspect_combined_result.empty:
            print('No results combining ALL of those keyword terms, breaking. Try reducing number of terms or respelling.',
                 'Note no semiology dictionary is used.')
            break

    # clean up all nan columns
    inspect_combined_result = inspect_combined_result.dropna(axis='columns', how='all')
    return inspect_combined_result
