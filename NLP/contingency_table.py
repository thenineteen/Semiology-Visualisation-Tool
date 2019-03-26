import numpy as np
import matplotlib.pyplot as plt
import seaborn as sn
import pandas as pd
import os
from scipy.stats import chi2_contingency

def chi_squared_yates(
                      no_Gold, no_No_Surgery, no_Resections,
                      no_Gold_absent_term, no_No_Surgery_absent_term, no_Resections_absent_term
                      ):
    """
    "Chi-Squared Yates correction: chi2-stat, p-value, DOF, expected ndarray same shape as contingency table"
    Returns text to add to contingency table. 
    """
    obs = np.array([
                    [no_Gold, no_No_Surgery + no_Resections], 
                    [no_Gold_absent_term, no_No_Surgery_absent_term + no_Resections_absent_term]
                    ])

    chi_sq, p_value, dof, exp_arr = chi2_contingency(obs)
    # table_chi_sq_text = str("Chi-Sq-stat = ") + str(round(chi_sq,2))
    
    if p_value <0.001:
        table_chi_sq_text = "****"
    elif p_value <0.01:
        table_chi_sq_text = "***"
    elif p_value <0.025:
        table_chi_sq_text = "**"
    elif p_value <0.05:
        table_chi_sq_text = "*"    
    else:
        pass
    
    return table_chi_sq_text


def contingency_table_two_outcomes(term,
                      no_Gold, no_No_Surgery, no_Resections,
                      no_Gold_absent_term, no_No_Surgery_absent_term, no_Resections_absent_term,
                      save_to_folder='L:\\word_docs\\NLP\\contingency_tables\\'):

    conf_arr = np.array([
                        [no_Gold, no_No_Surgery + no_Resections], 
                        [no_Gold_absent_term, no_No_Surgery_absent_term + no_Resections_absent_term]
                        ])

    df_cm = pd.DataFrame(conf_arr, 
                    index = ['absent', 'present'],
                    columns = ['Entirely Seizure-Free', 'Not Seizure-Free'])

    fig = plt.figure()

    plt.clf()

    ax = fig.add_subplot(111)

    ax.set_aspect(1)

    res = sn.heatmap(df_cm, annot=True, vmin=0.0, vmax=100.0, fmt='.0f')

    plt.yticks([0.5,1.5], ['term present', 'term absent'],va='center')

    plt.title('''Contingency Table \n Gold vs non-Gold \n Term: {} 
            '''.format(term))
    
    # add chi-squared text to the top left cell in 2 by 2 table
    table_chi_sq_text = chi_squared_yates(                     
                                          no_Gold, no_No_Surgery, no_Resections,
                                          no_Gold_absent_term, no_No_Surgery_absent_term, no_Resections_absent_term)
    left, width = .25, .5
    bottom, height = .25, .5
    right = left + width
    top = bottom + height
    ax.text(
            0.25*(left+right), 0.65*(bottom+top), table_chi_sq_text,
            horizontalalignment='center',
            verticalalignment='center',
            fontsize=20, color='black',
            transform=ax.transAxes)


    filename = 'confusion_table_' + str(term) + '.png'
    filename_and_path = os.path.join(save_to_folder, filename)
    plt.savefig(filename_and_path, format='png', bbox_inches='tight')