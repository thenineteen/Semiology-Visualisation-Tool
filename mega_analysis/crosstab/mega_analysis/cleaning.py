def cleaning(df):

    """
    perform checks and clean imported df
    Ali Alim-Marvasti July 2019
    """

    print('df.shape to begin with:', df.shape)
    print('Removing empty rows and columns:')

    post_op = 'Post-op Sz Freedom (Engel Ia, Ib; ILAE 1, 2)'
    concordant = 'Concordant Neurophys & Imaging (MRI, PET, SPECT)'
    # sEEG_ES = 'sEEG and/or ES'  # July 2019 version
    sEEG_ES = 'sEEG (y) and/or ES (ES)'  # March 2020 version
    keep_columns = [post_op, concordant, sEEG_ES]


    cfirst = list(df.columns)
    ifirst = list(df.index)

    # this part purely to allow exclusions.py to exclude concordant without messing up np.nan or using zeros
    cols = [col for col in list(df.columns) if col not in keep_columns]
    a = df[cols].copy()
    a.dropna(axis=1, how='all', inplace=True) # columns
    # now re attach the keep_columns
    b = df[keep_columns]
    df = b.merge(a, right_index=True, left_index=True)

        # df = df.dropna(axis=0, how='all')  # index
    df.dropna(axis=0, how='all', inplace=True)  # March 2020 version

    csecond=list(df.columns)
    isecond=list(df.index)
    print('\t', len(cfirst) - len(csecond), 'empty anatomical labels=columns')  # 20 empty anatomical labels
    print('\t', len(ifirst) - len(isecond), "empty rows=empty lines")  # 58 empty rows

    print('df.shape after dropna:', df.shape)

    print('\n')
    print('THESE ARE THE REMOVED EMPTY LABELS:\n')
    for c in cfirst:
        if c not in csecond:
            print(c)

    return df