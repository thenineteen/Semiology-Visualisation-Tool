# 16/4/19

import pickle

import sys
sys.path.insert(0, r"C:\Users\ali_m\AnacondaProjects\PhD\Epilepsy_Surgery_Project")

from NLP.term_phrase_outcome_cycle_many_terms import *
from NLP.term_phrase_negation_second_pass import *
from NLP.contingency_table import *

from crosstab.Semiology_Crosstab.Semiology_Crosstab_exclude_files_with_outcome_8 import *
from crosstab.Semiology_Crosstab.main_dataframe import *
from crosstab.Semiology_Crosstab.populate_main_dataframe import *
from crosstab.outcomes import *

# load all pickled data including dataframes

def openpickle(path_to_file):
    with open(path_to_file, 'rb') as f:
        data = pickle.load(f)

    return data



def imports():
    path_to_file2 = 'L:\\word_docs\\NLP\\Data Pickles\\gold_outcomes_list.pickle'
    path_to_file3 = 'L:\\word_docs\\NLP\\Data Pickles\\had_surgery_exclusions.pickle'
    path_to_file4 = 'L:\\word_docs\\NLP\\Data Pickles\\automated\\updated dataframes\\df.pickle'
    path_to_file5 = 'L:\\word_docs\\NLP\\Data Pickles\\automated\\updated dataframes\\df_No_surgery.pickle'
    path_to_file6 = 'L:\\word_docs\\NLP\\Data Pickles\\automated\\updated dataframes\\df_word_xduplicated_noredundantcolumns_noHx.pickle'
    path7 = 'L:\\word_docs\\NLP\\Data Pickles\\automated\\updated dataframes\\df_word_xduplicated_noredundantcolumns_noHx_binary.pickle'
    path8 = 'L:\\word_docs\\NLP\\Data Pickles\\automated\\updated dataframes\\X_gold.pickle'
    path9 = 'L:\\word_docs\\NLP\\Data Pickles\\automated\\updated dataframes\\y_gold.pickle'


    gold_outcomes_list = openpickle(path_to_file2)
    _, had_surgery_MRNs = gold_outcomes_MRNs()
    had_surgery_exclusions = openpickle(path_to_file3)

    df = openpickle(path_to_file4)
    df_word_xduplicated_noredundantcolumns_noHx = openpickle(path_to_file6)
    df_word_xduplicated_noredundantcolumns_noHx_binary = openpickle(path7)
    X_gold = openpickle(path8)
    y_gold = openpickle(path9)

    df_No_surgery = openpickle(path_to_file5)


    return (gold_outcomes_list,
            (_, had_surgery_MRNs),
            had_surgery_exclusions,
            df,
            df_word_xduplicated_noredundantcolumns_noHx,
            df_word_xduplicated_noredundantcolumns_noHx_binary,
            X_gold,
            y_gold,
            df_No_surgery)



def LRCV5_refit_False(X_gold,y_gold):
    clf_gold_cv = LogisticRegressionCV(cv=5, refit=False).fit(X_gold, y_gold)
    y_pred_gold_cv = clf_gold_cv.predict(X_gold)
    cm = confusion_matrix(y_gold, y_pred_gold_cv)
    print('accuracy:', clf_gold_cv.score(X_gold, y_gold), '\ny_gold shape:', y_gold.shape,
        '\ncm:\n', cm,
        '\nnumber of fx:', X_gold.shape[1],
        'AUC', auc)

    return clf_gold_cv
