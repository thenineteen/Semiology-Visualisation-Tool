import numpy as np
import matplotlib.pyplot as plt
import seaborn as sn
import pandas as pd
import os
from scipy.stats import chi2_contingency

def chi_squared_yates(
                      no_Gold, no_Resections, no_No_Surgery,
                      no_Gold_absent_term, no_Resections_absent_term, no_No_Surgery_absent_term,
                      two_outcomes=True, print_numbers=False):
    """
    "Chi-Squared Yates correction: chi2-stat, p-value, DOF, expected ndarray same shape as contingency table"
    Returns text to add to contingency table. 
    """
    if two_outcomes:
        obs = np.array([
                        [no_Gold, no_No_Surgery + no_Resections], 
                        [no_Gold_absent_term, no_No_Surgery_absent_term + no_Resections_absent_term]
                        ])

    else: 
        # three outcomes
        obs = np.array([
                        [no_Gold,  no_Resections, no_No_Surgery], 
                        [no_Gold_absent_term, no_Resections_absent_term, no_No_Surgery_absent_term]
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
        table_chi_sq_text = "-"
    
    if print_numbers:
        print("Chi-Squared with Yates correction:")
        print("chi2-stat =\t{}".format(chi_sq)) 
        print("p-value =\t{}".format(p_value))
        print("DOF =\t{}".format(dof))
        print("expected ndarray same shape as contingency table = \n{}".format(exp_arr))
    

    stats_string = "chi2-stat = " + str(round(chi_sq,3)) +\
        "\np-value = " + str(round(p_value,9)) +\
        "\nDOF = " + str(dof) +\
        "\nexpected ndarray = \n" + str(np.around(exp_arr))
    
        
    return table_chi_sq_text, stats_string


def contingency_table_two_outcomes(term, 
                      no_Gold, no_Resections, no_No_Surgery,
                      no_Gold_absent_term, no_Resections_absent_term, no_No_Surgery_absent_term,
                      save_to_folder='L:\\word_docs\\NLP\\contingency_tables\\',
                      print_numberss=False,
                      eps=False,
                      term_regex_str=""):

    if not term_regex_str:
        term_regex_str = "term"

    conf_arr = np.array([
                        [no_Gold, no_No_Surgery + no_Resections], 
                        [no_Gold_absent_term, no_No_Surgery_absent_term + no_Resections_absent_term]
                        ])

    df_cm = pd.DataFrame(conf_arr, 
                    index = ['present', 'absent'],
                    columns = ['Entirely Seizure-Free', 'Other'])

    fig = plt.figure()

    plt.clf()

    ax = fig.add_subplot(121)
    fig.tight_layout()

    ax.set_aspect(1)

    res = sn.heatmap(df_cm, annot=True, vmin=0.0, vmax=100.0, fmt='.0f')

    plt.yticks([0.5,1.5], [term_regex_str + ' present', 'absent'], va='center')

    plt.title('''Contingency Table \n Term: {} 
            '''.format(term))
    
    # add chi-squared test *'s to the top left cell in 2 by 2 table
    table_chi_sq_text, stats_string = chi_squared_yates(                     
                                          no_Gold, no_Resections, no_No_Surgery,
                                          no_Gold_absent_term, no_Resections_absent_term, no_No_Surgery_absent_term,
                                          print_numbers=print_numberss)
    left, width = .25, .5
    bottom, height = .25, .5
    right = left + width
    top = bottom + height
    ax.text(
            0.25*(left+right), 0.65*(bottom+top), table_chi_sq_text,
            horizontalalignment='center',
            verticalalignment='center',
            fontsize=15, color='black',
            transform=ax.transAxes)


    # add subplot with only text of stats read out
    ax2 = fig.add_subplot(122)
    plt.title('''Chi-Squared with Yates correction''')
    ax2.text(0.4*(left+right), 0.8*(bottom+top), stats_string,
             horizontalalignment='center',
             verticalalignment='center',
             fontsize=9, color='black')
    # #remove axes
    sn.despine(left=True, top=True, right=True, bottom=True)
    #ax.set_frame_on(False)
    plt.axis('off')


    # save
    if eps:
        filename = 'confusion_table_2_' + str(term) + '.eps'
        filename_and_path = os.path.join(save_to_folder, filename)
        plt.savefig(filename_and_path, format='eps', bbox_inches='tight', dpi=1200)

    else:
        filename = 'confusion_table_2_' + str(term) + '.png'
        filename_and_path = os.path.join(save_to_folder, filename)
        plt.savefig(filename_and_path, format='png', bbox_inches='tight')






def contingency_table_three_outcomes(term,
                      no_Gold, no_Resections, no_No_Surgery,
                      no_Gold_absent_term, no_Resections_absent_term, no_No_Surgery_absent_term,
                      save_to_folder='L:\\word_docs\\NLP\\contingency_tables\\',
                      print_numberss=False,
                      eps=False,
                      term_regex_str=""):
    
    conf_arr = np.array([
                        [no_Gold, no_Resections, no_No_Surgery], 
                        [no_Gold_absent_term, no_Resections_absent_term, no_No_Surgery_absent_term]
                        ])

    df_cm = pd.DataFrame(conf_arr, 
                    index = ['present', 'absent'],
                    columns = ['Entirely Seizure-Free', 'Resections', 'No Surgery'])

    fig = plt.figure()

    plt.clf()

    ax = fig.add_subplot(121)
    fig.tight_layout()

    ax.set_aspect(1)

    res = sn.heatmap(df_cm, annot=True, vmin=0.0, vmax=100.0, fmt='.0f')

    plt.yticks([0.5,1.5], [term_regex_str + ' present', 'absent'],va='center')

    plt.title('''Contingency Table \n Term: {} 
            '''.format(term))
    
    # add chi-squared *'s to the top left cell in 2 by 2 table
    table_chi_sq_text, stats_string = chi_squared_yates(                     
                                          no_Gold, no_Resections, no_No_Surgery,
                                          no_Gold_absent_term, no_Resections_absent_term, no_No_Surgery_absent_term,
                                          two_outcomes=False, print_numbers=print_numberss)
    left, width = .25, .5
    bottom, height = .25, .5
    right = left + width
    top = bottom + height
    ax.text(
            0.5*0.33*(left+right), 0.65*(bottom+top), table_chi_sq_text,
            horizontalalignment='center',
            verticalalignment='center',
            fontsize=15, color='black',
            transform=ax.transAxes)


    # add subplot with only text of stats read out
    ax2 = fig.add_subplot(122)
    plt.title('''Chi-Squared''')
    ax2.text(0.4*(left+right), 0.8*(bottom+top), stats_string,
             horizontalalignment='center',
             verticalalignment='center',
             fontsize=9, color='black')
    # #remove axes
    sn.despine(left=True, top=True, right=True, bottom=True)
    #ax.set_frame_on(False)
    plt.axis('off')


    # save
    if eps:
        filename = 'confusion_table_3_' + str(term) + '.eps'
        filename_and_path = os.path.join(save_to_folder, filename)
        plt.savefig(filename_and_path, format='eps', bbox_inches='tight', dpi=1200)

    else:
        filename = 'confusion_table_3_' + str(term) + '.png'
        filename_and_path = os.path.join(save_to_folder, filename)
        plt.savefig(filename_and_path, format='png', bbox_inches='tight')