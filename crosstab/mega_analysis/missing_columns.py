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
            print('\n\t', '\"',col,'\"', 'missing values:')

            print( df.loc[ df[col].isna(), ['Reference', 'Reported Semiology', 'Semiology Category']])