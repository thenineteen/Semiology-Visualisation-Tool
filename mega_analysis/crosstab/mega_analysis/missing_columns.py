def missing_columns(df,
    default_cols = ['Reported Semiology', 'Semiology Category'],
    ):

    """
    These columns must always have a value. 
    """

    for col in default_cols:

        if df[col].isna().sum() ==0:
            print('\n\t', col, 'no missing values')

        else: 
            print('\n\t', 'missing', col, ' descriptions:')

            print( df.loc[ df[col].isna().index, 'Reference'] )