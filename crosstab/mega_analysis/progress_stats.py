import pandas as pd
import matplotlib.pyplot as plt
from matplotlib_venn import venn3

def progress_stats(df):
    """
    Progress stats from the df by ground truths.
    If error, check the column names.

    Ground Truth: looks at concordance, sEEG/stimulation and seizure-free inclusion criteria

    note in pandas 0.24+ .nonzero() needs to be replaced with .to_numpy().nonzero() 

    Ali Alim-Marvasti July, August 2019
    """

    # initialise: first three are the excel file column names
    post_op = 'Post-op Sz Freedom (Engel Ia, Ib; ILAE 1, 2)'
    concordant = 'Concordant Neurophys & Imaging (MRI, PET, SPECT)'
    sEEG_ES = 'sEEG and/or ES'
    
    # initialise the df_ground_truths df:
    colx = pd.MultiIndex.from_product([['Lateralising Datapoints', 'Localising Datapoints'], ['Exclusive', 'Total']],
                                   #names=['year', 'visit']
                                 )
    df_ground_truths = pd.DataFrame(columns=colx)
    
    
    # populate the total df:
    df_ground_truths.loc['Seizure-Free', ('Lateralising Datapoints', 'Total')] = df.loc[df[post_op].notnull()].Lateralising.sum()
    df_ground_truths.loc['Seizure-Free', ('Localising Datapoints', 'Total')] = df.loc[df[post_op].notnull()].Localising.sum()

    df_ground_truths.loc['Concordant', ('Lateralising Datapoints', 'Total')] = df.loc[df[concordant].notnull()].Lateralising.sum()
    df_ground_truths.loc['Concordant', ('Localising Datapoints', 'Total')] = df.loc[df[concordant].notnull()].Localising.sum()

    df_ground_truths.loc['sEEG and|or ES', ('Lateralising Datapoints', 'Total')] = df.loc[df['sEEG and/or ES'].notnull()].Lateralising.sum()
    df_ground_truths.loc['sEEG and|or ES', ('Localising Datapoints', 'Total')] = df.loc[df['sEEG and/or ES'].notnull()].Localising.sum()

    df_ground_truths.loc['ES', ('Lateralising Datapoints', 'Total')] = df.loc[df[sEEG_ES]== 'ES'].Lateralising.sum()
    df_ground_truths.loc['ES', ('Localising Datapoints', 'Total')] = df.loc[df[sEEG_ES]== 'ES'].Localising.sum()
    
    
    # populate the exlusives:
    df_ground_truths.loc['Seizure-Free', ('Lateralising Datapoints', 'Exclusive')] = df.loc[(
        df[post_op].notnull() & df[concordant].isnull() & df[sEEG_ES].isnull()
        ) ].Lateralising.sum()
    df_ground_truths.loc['Seizure-Free', ('Localising Datapoints', 'Exclusive')] = df.loc[(
         df[post_op].notnull() & df[concordant].isnull() & df[sEEG_ES].isnull()
        ) ].Localising.sum()
    df_ground_truths.loc['Concordant', ('Lateralising Datapoints', 'Exclusive')] = df.loc[(
         df[concordant].notnull() & df[post_op].isnull() & df[sEEG_ES].isnull()
        ) ].Lateralising.sum()
    df_ground_truths.loc['Concordant', ('Localising Datapoints', 'Exclusive')] = df.loc[(
        df[concordant].notnull() & df[post_op].isnull() & df[sEEG_ES].isnull()
        ) ].Localising.sum()
    df_ground_truths.loc['sEEG and|or ES', ('Lateralising Datapoints', 'Exclusive')] = df.loc[(
        df[sEEG_ES].notnull() & df[post_op].isnull() & df[concordant].isnull()
        ) ].Lateralising.sum()
    df_ground_truths.loc['sEEG and|or ES', ('Localising Datapoints', 'Exclusive')] = df.loc[(
        df[sEEG_ES].notnull() & df[post_op].isnull() & df[concordant].isnull()
        ) ].Localising.sum()
    df_ground_truths.loc['ES', ('Lateralising Datapoints', 'Exclusive')] = df.loc[(
        (df[sEEG_ES]=='ES') & df[post_op].isnull() & df[concordant].isnull()
        ) ].Lateralising.sum()
    df_ground_truths.loc['ES', ('Localising Datapoints', 'Exclusive')] = df.loc[(
         (df[sEEG_ES]=='ES') & df[post_op].isnull() & df[concordant].isnull()
        ) ].Localising.sum()

    # All Combinations e.g. sz free and concordant and other combinations:
    df_ground_truths.loc['Seizure-Free & Concordant', ('Lateralising Datapoints', 'Exclusive')] = df.loc[(
        df[post_op].notnull() & df[concordant].notnull() & df[sEEG_ES].isnull()
        ) ].Lateralising.sum()
    df_ground_truths.loc['Seizure-Free & Concordant', ('Localising Datapoints', 'Exclusive')] = df.loc[(
        df[post_op].notnull() & df[concordant].notnull() & df[sEEG_ES].isnull()
        ) ].Localising.sum()

    df_ground_truths.loc['Seizure-Free & sEEG/ES', ('Lateralising Datapoints', 'Exclusive')] = df.loc[(
        df[post_op].notnull() & df[concordant].isnull() & df[sEEG_ES].notnull()
        ) ].Lateralising.sum()
    df_ground_truths.loc['Seizure-Free & sEEG/ES', ('Localising Datapoints', 'Exclusive')] = df.loc[(
        df[post_op].notnull() & df[concordant].isnull() & df[sEEG_ES].notnull()
        ) ].Localising.sum()

    df_ground_truths.loc['Concordant & sEEG/ES', ('Lateralising Datapoints', 'Exclusive')] = df.loc[(
        df[post_op].isnull() & df[concordant].notnull() & df[sEEG_ES].notnull()
        ) ].Lateralising.sum()
    df_ground_truths.loc['Concordant & sEEG/ES', ('Localising Datapoints', 'Exclusive')] = df.loc[(
        df[post_op].isnull() & df[concordant].notnull() & df[sEEG_ES].notnull()
        ) ].Localising.sum()

    df_ground_truths.loc['All three', ('Lateralising Datapoints', 'Exclusive')] = df.loc[(
        df[post_op].notnull() & df[concordant].notnull() & df[sEEG_ES].notnull()
        ) ].Lateralising.sum()
    df_ground_truths.loc['All three', ('Localising Datapoints', 'Exclusive')] = df.loc[(
        df[post_op].notnull() & df[concordant].notnull() & df[sEEG_ES].notnull()
        ) ].Localising.sum()
    
    return df_ground_truths


def progress_venn(df_ground_truths, method=None):
    """
    Use the progress df to plot a venn diagram of the datapoints by ground truths.

    arguments:
    ---
    method: "Lateralising" or "Localising"
    ---

    Ali Alim-Marvasti July 2019
    """


    if method==None:
        print('progress_venn needs a method specified')
        return
    elif method=='Lateralising':
        method='Lateralising Datapoints'
    elif method=='Localising':
        method='Localising Datapoints'

    # use the df to find the venn numbers
    sz_excl = df_ground_truths.loc['Seizure-Free', (method, 'Exclusive')]
    conc_excl = df_ground_truths.loc['Concordant', (method, 'Exclusive')]
    sz_conc = df_ground_truths.loc['Seizure-Free & Concordant', (method, 'Exclusive')]
    sEEG_excl = df_ground_truths.loc['sEEG and|or ES', (method, 'Exclusive')]
    sEEG_ES_sz = df_ground_truths.loc['Seizure-Free & sEEG/ES', (method, 'Exclusive')]
    sEEG_ES_conc = df_ground_truths.loc['Concordant & sEEG/ES', (method, 'Exclusive')]
    all_three = df_ground_truths.loc['All three', (method, 'Exclusive')]

    # set a tuple
    numbers = (sz_excl, conc_excl, sz_conc, sEEG_excl, sEEG_ES_sz, sEEG_ES_conc, all_three)
    a = [int(n) for n in numbers]
    numbers = tuple(a)
    # plot
    venn3(subsets = (numbers), set_labels = ('Seizure-Free', 'Concordant', 'sEEG/ES'))
    titre = method + ' by Ground Truth'
    plt.title(titre)
    plt.show()
