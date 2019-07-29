import pandas as pd 

def QUERY_SEMIOLOGY(df, semiology_term='love', ignore_case=True):
    """
    Search for key terms in both reported and categories of semiologies and return df if found in either.
    Removes all columns which are entirely null. 
    
    """
    
    if ignore_case:
        semiology_term = r'(?i)'+semiology_term

    reported_semiology = df.loc[df['Reported Semiology'].str.contains(semiology_term, na=False)]
    inspect_result = reported_semiology.append(
        df.loc[df['Semiology Category'].str.contains(semiology_term, na=False)]
        )
        
    inspect_result = inspect_result.dropna(axis='columns', how='all')
    inspect_result.drop_duplicates(inplace=True)

    return inspect_result