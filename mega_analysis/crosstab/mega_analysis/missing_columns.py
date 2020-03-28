import logging

def missing_columns(df,
    default_cols = ['Reported Semiology', 'Semiology Category'],
    ):

    """
    These columns must always have a value.
    """

    for col in default_cols:

        if df[col].isna().sum() ==0:
            logging.debug(f'\n\t {col} no missing values')

        else:
            logging.debug('\n\t {missing} {col} descriptions:')

            logging.debug(str(df.loc[ df[col].isna().index, 'Reference']))
