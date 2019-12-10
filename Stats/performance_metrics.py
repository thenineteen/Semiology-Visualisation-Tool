import pandas as pd
import numpy as np
from scipy.stats import chi2, chisquare, fisher_exact, chi2_contingency

def performance_metrics(df, col, target):
    """
    Setting Univariate Benchmarks using DataFrame
    col = feature we are intersted in
    target = what we are predicting (col of df)
    df: rows= patients, cols = features

    Marvasti Dec 2020
    """


    no_of_pts_with_semiology_and_target_outcome = df.loc[df[col]==1, target].sum()
    total_with_semio = df.loc[df[col]==1, target].count()
    total_with_target = df.loc[df[target]==1, col].sum()
    total_patients = df.shape[0]

    col_y_target_y = no_of_pts_with_semiology_and_target_outcome
    col_y_target_n = total_with_semio - no_of_pts_with_semiology_and_target_outcome 
    # col_n_target_y = total_with_target - no_of_pts_with_semiology_gold
    col_n_target_y = df.loc[((df[target]==1)&(df[col]==0)), target].count()  # equivalent to .sum()
    col_n_target_n = df.loc[((df[target]==0)&(df[col]==0)), target].count()

    
    print('variable being tested: ', col, ' target: ', target)
    if col_y_target_n == (df.loc[((df[target]==0)&(df[col]==1)), target].count()) :
        print ('integrity check : pass')
    else: 
        print('oops major probelmo: not adding up. see source')
    

    OR_fisher, pv_fisher = fisher_exact(
        [
        [col_y_target_y, col_y_target_n],
        [col_n_target_y, col_n_target_n]
        ]         ) 
    
    OR_chi, pv_chi, _, _ = chi2_contingency(
        [
        [col_y_target_y, col_y_target_n],
        [col_n_target_y, col_n_target_n]
        ]         )

    OR_manual = (col_y_target_y/col_y_target_n) / (col_n_target_y/col_n_target_n)


    SENS = col_y_target_y/(col_y_target_y+col_n_target_y)

    SPEC = col_n_target_n/(col_y_target_n+col_n_target_n)

    PPV = col_y_target_y/(col_y_target_y+col_y_target_n)

    NPV = col_n_target_n/(col_n_target_y+col_n_target_n)

    f1_score_target_y = 2*(SENS)*(PPV)/(SENS+PPV)

    f1_score_target_n = 2*(SPEC)*(NPV)/(SPEC+NPV)

    F1_MACRO = (f1_score_target_y+f1_score_target_n)/2

    BAL_ACC = (SENS+SPEC)/2

    ACCURACY_simple = (col_y_target_y+col_n_target_n)/(col_y_target_y+col_n_target_n+col_y_target_n+col_n_target_y)

  
    metrics_OR = {'OR_fisher': OR_fisher, 'OR_chi':OR_chi ,  'OR_manual': OR_manual}
    metrics_classic = {'SENS':SENS, 'SPEC':SPEC, 'PPV':PPV, 'NPV':NPV, 'F1_MACRO':F1_MACRO,  'BAL_ACC':BAL_ACC, 
        'ACCURACY_simple':ACCURACY_simple}

    for i in metrics_OR.keys():
        print(i, metrics_OR[i])

    for j in metrics_classic.keys():
        print(j, metrics_classic[j])
