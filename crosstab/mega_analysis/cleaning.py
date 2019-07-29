def cleaning(df):

    """
    perform checks and clean imported df
    Ali Alim-Marvasti July 2019
    """

    print('df.shape to begin with:', df.shape)
    print('Removing empty rows and columns:')

    cfirst = df.columns
    ifirst = df.index

    df = df.dropna(axis=0, how='all')  # index
    df = df.dropna(axis=1, how='all')  # columns

    csecond=df.columns
    isecond=df.index
    print('\t', len(cfirst) - len(csecond), 'empty anatomical labels=columns')  # 20 empty anatomical labels
    print('\t', len(ifirst) - len(isecond), "empty rows=empty lines")  # 58 empty rows

    print('df.shape after dropna:', df.shape)

    print('\n')
    print('THESE ARE THE REMOVED EMPTY LABELS:\n')
    for c in cfirst:
        if c not in csecond:
            print(c)

    return df