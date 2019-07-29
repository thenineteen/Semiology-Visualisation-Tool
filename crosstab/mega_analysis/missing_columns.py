def missing_columns(df,
    default_cols = ['Reported Semiology', 'Semiology Category'],
    ):

    """
    These columns must have a value always. 
    """

    for col in default_cols:

        if df[col].isna().sum() ==0:
            print('\n\t', col, 'no missing labels')

        else: 
            print('\n\t', '(',col,')', 'missing labels:')

            print( df.loc[ df[col].isna(), ['Reference', 'Reported Semiology', 'Semiology Category']])