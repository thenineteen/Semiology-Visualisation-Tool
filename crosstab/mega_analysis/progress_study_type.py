import pandas as pd
import matplotlib.pyplot as plt
from matplotlib_venn import venn3

def progress_study_type(df):
    """
    Similar to progress_stats but not about ground truths, 
    rather about Bayesian priors in publications i.e. pt selections criteria.

    Study Type: look at the broad selection criteria for the study: 
                patients selected by lobe "Epilepsy Topology"
                patients unselected or selected by semiology "Spontaneous Semiology"
                patients who underwent cortical electrical stimulation
                and patients selected based on other criteria (e.g. autoimmune antibodies or genetics)

    (Note that sEEG is a recording inclusion criteria (ground truth) but not a study type.) 
    """

    # initialise: first three are the excel file column names
    CES = 'Cortical Stimulation (CS)'
    SS = 'Spontaneous Semiology (SS)'
    ET = 'Epilepsy Topology (ET)'
    OTHER = 'Other (e.g. Abs)'
    
    # initialise the df_study_type df:
    colx = pd.MultiIndex.from_product([['Lateralising Datapoints', 'Localising Datapoints'], ['Exclusive', 'Total']],
                                   #names=['year', 'visit']
                                 )
    df_study_type = pd.DataFrame(columns=colx)
    
    
    # populate the total df:
    df_study_type.loc['Cortical Stimulation', ('Lateralising Datapoints', 'Total')] = df.loc[df[CES].notnull()].Lateralising.sum()
    df_study_type.loc['Cortical Stimulation', ('Localising Datapoints', 'Total')] = df.loc[df[CES].notnull()].Localising.sum()

    df_study_type.loc['Semiological', ('Lateralising Datapoints', 'Total')] = df.loc[df[SS].notnull()].Lateralising.sum()
    df_study_type.loc['Semiological', ('Localising Datapoints', 'Total')] = df.loc[df[SS].notnull()].Localising.sum()

    df_study_type.loc['Topological', ('Lateralising Datapoints', 'Total')] = df.loc[df[ET].notnull()].Lateralising.sum()
    df_study_type.loc['Topological', ('Localising Datapoints', 'Total')] = df.loc[df[ET].notnull()].Localising.sum()

    df_study_type.loc['OTHER', ('Lateralising Datapoints', 'Total')] = df.loc[df[OTHER].notnull()].Lateralising.sum()
    df_study_type.loc['OTHER', ('Localising Datapoints', 'Total')] = df.loc[df[OTHER].notnull()].Localising.sum()
    
    
    # populate the exlusives:
    df_study_type.loc['Cortical Stimulation', ('Lateralising Datapoints', 'Exclusive')] = df.loc[(
        df[CES].notnull() & df[SS].isnull() & df[ET].isnull() 
        ) ].Lateralising.sum()
    df_study_type.loc['Cortical Stimulation', ('Localising Datapoints', 'Exclusive')] = df.loc[(
         df[CES].notnull() & df[SS].isnull() & df[ET].isnull() 
        ) ].Localising.sum()
    df_study_type.loc['Semiological', ('Lateralising Datapoints', 'Exclusive')] = df.loc[(
         df[SS].notnull() & df[CES].isnull() & df[ET].isnull() 
        ) ].Lateralising.sum()
    df_study_type.loc['Semiological', ('Localising Datapoints', 'Exclusive')] = df.loc[(
        df[SS].notnull() & df[CES].isnull() & df[ET].isnull() 
        ) ].Localising.sum()
    df_study_type.loc['Topological', ('Lateralising Datapoints', 'Exclusive')] = df.loc[(
        df[ET].notnull() & df[CES].isnull() & df[SS].isnull() 
        ) ].Lateralising.sum()
    df_study_type.loc['Topological', ('Localising Datapoints', 'Exclusive')] = df.loc[(
        df[ET].notnull() & df[CES].isnull() & df[SS].isnull() 
        ) ].Localising.sum()
    df_study_type.loc['OTHER', ('Lateralising Datapoints', 'Exclusive')] = df.loc[(
        (df[OTHER]).notnull() & df[CES].isnull() & df[SS].isnull() & df[ET].isnull()
        ) ].Lateralising.sum()
    df_study_type.loc['OTHER', ('Localising Datapoints', 'Exclusive')] = df.loc[(
         (df[OTHER]).notnull() & df[CES].isnull() & df[SS].isnull() & df[ET].isnull()
        ) ].Localising.sum()

    # All Combinations EXCLUDING OTHER:
    df_study_type.loc['Cortical Stimulation & Semiological', ('Lateralising Datapoints', 'Exclusive')] = df.loc[(
        df[CES].notnull() & df[SS].notnull() & df[ET].isnull() 
        ) ].Lateralising.sum()
    df_study_type.loc['Cortical Stimulation & Semiological', ('Localising Datapoints', 'Exclusive')] = df.loc[(
        df[CES].notnull() & df[SS].notnull() & df[ET].isnull() 
        ) ].Localising.sum()
    df_study_type.loc['Cortical Stimulation & Topological', ('Lateralising Datapoints', 'Exclusive')] = df.loc[(
        df[CES].notnull() & df[ET].notnull() & df[SS].isnull() 
        ) ].Lateralising.sum()
    df_study_type.loc['Cortical Stimulation & Topological', ('Localising Datapoints', 'Exclusive')] = df.loc[(
        df[CES].notnull() & df[ET].notnull() & df[SS].isnull() 
        ) ].Localising.sum()


    df_study_type.loc['Semiological & Topological', ('Lateralising Datapoints', 'Exclusive')] = df.loc[(
        df[CES].isnull() & df[SS].notnull() & df[ET].notnull() 
        ) ].Lateralising.sum()
    df_study_type.loc['Semiological & Topological', ('Localising Datapoints', 'Exclusive')] = df.loc[(
        df[CES].isnull() & df[SS].notnull() & df[ET].notnull() 
        ) ].Localising.sum()

    #threes
    df_study_type.loc['CES, SS, ET', ('Lateralising Datapoints', 'Exclusive')] = df.loc[(
        df[CES].notnull() & df[SS].notnull() & df[ET].notnull()
        ) ].Lateralising.sum()
    df_study_type.loc['CES, SS, ET', ('Localising Datapoints', 'Exclusive')] = df.loc[(
        df[CES].notnull() & df[SS].notnull() & df[ET].notnull()
        ) ].Localising.sum()
    
    return df_study_type


def progress_venn_2(df_study_type, method=None):
    """
    Use the progress df to plot a venn diagram of the datapoints by study types (by ground truth is the original).

    arguments:
    ---
    method: "Lateralising" or "Localising"
    ---

    Ali Alim-Marvasti Aug 2019
    """


    if method==None:
        print('progress_venn4 needs a method specified')
        return
    elif method=='Lateralising':
        method='Lateralising Datapoints'
    elif method=='Localising':
        method='Localising Datapoints'

    # use the df to find the venn numbers
    ces_excl = df_study_type.loc['Cortical Stimulation', (method, 'Exclusive')]
    ss_excl = df_study_type.loc['Semiological', (method, 'Exclusive')]
    et_excl = df_study_type.loc['Topological', (method, 'Exclusive')]
   
    ces_ss = df_study_type.loc['Cortical Stimulation & Semiological', (method, 'Exclusive')]
    ces_et = df_study_type.loc['Cortical Stimulation & Topological', (method, 'Exclusive')] 
    
    ss_et =  df_study_type.loc['Semiological & Topological', (method, 'Exclusive')]

    ces_ss_et = df_study_type.loc['CES, SS, ET', (method, 'Exclusive')]

    # set a tuple
    numbers = (ces_excl, ss_excl, ces_ss,
                et_excl, ces_et, ss_et,
                ces_ss_et)
    a = [int(n) for n in numbers]
    numbers = tuple(a)
    # plot
    venn3(subsets = (numbers), set_labels = ('Stimulation', 'Semiological', 'Topological'))
    titre = method + ' by Patient Selection Priors (Study Type)'
    plt.title(titre)
    plt.show()

    