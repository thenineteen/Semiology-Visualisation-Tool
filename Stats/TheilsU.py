from collections import Counter
import math
from Stats.CramersV import *
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import entropy


# note for Theils u the given is the x or columns. so entropy of (y|x)
def conditional_entropy(x, y):
    """
    Calculates the conditional entropy of x given y: S(x|y)
    Wikipedia: https://en.wikipedia.org/wiki/Conditional_entropy
    **Returns:** float
    Parameters
    ----------
    x : list / NumPy ndarray / Pandas Series
        A sequence of measurements
    y : list / NumPy ndarray / Pandas Series
        A sequence of measurements
    """
    y_counter = Counter(y)
    xy_counter = Counter(list(zip(x,y)))
    total_occurrences = sum(y_counter.values())
    entropy = 0.0
    for xy in xy_counter.keys():
        p_xy = xy_counter[xy] / total_occurrences
        p_y = y_counter[xy[1]] / total_occurrences
        entropy += p_xy * math.log(p_y/p_xy)
#         entropy += p_xy * math.log(p_xy) # ali changed
    return entropy


def TheilsU(x, y):
    """
    Calculates Theil's U statistic (Uncertainty coefficient) for categorical-categorical association.
    This is the uncertainty of x given y: value is on the range of [0,1] - where 0 means y provides no information about
    x, and 1 means y provides full information about x.
    This is an asymmetric coefficient: U(x,y) != U(y,x)
    Wikipedia: https://en.wikipedia.org/wiki/Uncertainty_coefficient
    **Returns:** float in the range of [0,1]
    Parameters
    ----------
    x : list / NumPy ndarray / Pandas Series
        A sequence of categorical measurements
    y : list / NumPy ndarray / Pandas Series
        A sequence of categorical measurements
    """
    s_xy = conditional_entropy(x,y)
    x_counter = Counter(x)
    total_occurrences = sum(x_counter.values())
    p_x = list(map(lambda n: n/total_occurrences, x_counter.values()))
    s_x = entropy(p_x)
    if s_x == 0:
        return 1
    else:
        return (s_x - s_xy) / s_x


# https://github.com/shakedzy/dython/blob/master/build/lib/dython/nominal.py

def associations(dataset, nominal_columns=None, mark_columns=False, Theils_U=False, plot=True,
                          return_results = False, 
                          savefigure=False,
                          title_auto=False,
                          **kwargs):
    """
    Calculate the correlation/strength-of-association of features in data-set with both categorical (eda_tools) and
    continuous features using:
     * Pearson's R for continuous-continuous cases
     * Correlation Ratio for categorical-continuous cases
     * Cramer's V or Theil's U for categorical-categorical cases
    **Returns:** a DataFrame of the correlation/strength-of-association between all features
    **Example:** see `associations_example` under `dython.examples`
    Parameters
    ----------
    dataset : NumPy ndarray / Pandas DataFrame
        The data-set for which the features' correlation is computed
    nominal_columns : string / list / NumPy ndarray
        Names of columns of the data-set which hold categorical values. Can also be the string 'all' to state that all
        columns are categorical, or None (default) to state none are categorical
    mark_columns : Boolean, default = False
        if True, output's columns' names will have a suffix of '(nom)' or '(con)' based on there type (eda_tools or
        continuous), as provided by nominal_columns
    theil_u : Boolean, default = False
        In the case of categorical-categorical feaures, use Theil's U instead of Cramer's V
    plot : Boolean, default = True
        If True, plot a heat-map of the correlation matrix
    return_results : Boolean, default = False
        If True, the function will return a Pandas DataFrame of the computed associations
    kwargs : any key-value pairs
        Arguments to be passed to used function and methods


    use as such:
    associations(X, nominal_columns='all', mark_columns=False, TheilsU=True, plot=True,
                          return_results = False)
    """
    #dataset = convert(dataset, 'dataframe')
    columns = dataset.columns
    if nominal_columns is None:
        nominal_columns = list()
    elif nominal_columns == 'all':
        nominal_columns = columns
    corr = pd.DataFrame(index=columns, columns=columns)
    for i in range(0,len(columns)):
        for j in range(i,len(columns)):
            if i == j:
                corr[columns[i]][columns[j]] = 1.0
            else:
                if columns[i] in nominal_columns:
                    if columns[j] in nominal_columns:
                        if Theils_U:
                            corr[columns[j]][columns[i]] = TheilsU(dataset[columns[i]],dataset[columns[j]])
                            corr[columns[i]][columns[j]] = TheilsU(dataset[columns[j]],dataset[columns[i]])
                        else:
                            confusion_matrix = pd.crosstab(dataset[columns[i]],dataset[columns[j]])
                            cell = cramers_corrected_stat(confusion_matrix)
                            corr[columns[i]][columns[j]] = cell
                            corr[columns[j]][columns[i]] = cell
                    else:
                        cell = correlation_ratio(dataset[columns[i]], dataset[columns[j]])
                        corr[columns[i]][columns[j]] = cell
                        corr[columns[j]][columns[i]] = cell
                else:
                    if columns[j] in nominal_columns:
                        cell = correlation_ratio(dataset[columns[j]], dataset[columns[i]])
                        corr[columns[i]][columns[j]] = cell
                        corr[columns[j]][columns[i]] = cell
                    else:
                        cell, _ = pearsonr(dataset[columns[i]], dataset[columns[j]])
                        corr[columns[i]][columns[j]] = cell
                        corr[columns[j]][columns[i]] = cell
    corr.fillna(value=np.nan, inplace=True)
    if mark_columns:
        marked_columns = ['{} (nom)'.format(col) if col in nominal_columns else '{} (con)'.format(col) for col in columns]
        corr.columns = marked_columns
        corr.index = marked_columns
    if plot:
        plt.figure(figsize=kwargs.get('figsize',None))
        sns.heatmap(corr, annot=kwargs.get('annot',False), fmt=kwargs.get('fmt','.2f'), cmap='YlOrRd')
        
        if title_auto:
            # title = 'Categorical Correlation: Theil\'s U for top X%s of Diagnoses\n\%d Patients, %d Diagnoses'%("%", dataset.shape[0], dataset.shape[1])
            # title = 'Categorical Correlation: Theil\'s U Semiology, HS, EZ \n%d TEST patients, %d variables'%(dataset.shape[0], dataset.shape[1])
            title = 'Categorical Correlation: Cramer\'s V Semiology, HS, EZ \n%d TEST patients, %d variables'%(dataset.shape[0], dataset.shape[1])

        else:
            title = 'Title'
        plt.title(title)
        plt.xticks(np.arange(len(dataset.columns)), dataset.columns, rotation='vertical', fontsize=6, fontweight='ultralight')
        plt.yticks(np.arange(len(dataset.columns)), dataset.columns, fontsize=6)
        
        if savefigure:
            # plt.savefig('L:\\Parashkev_top_2%_TheilsU.eps', 
            #             format='eps', bbox_inches='tight', dpi=1200)

            plt.savefig('D:\\Ali USB Backup\\1 PhD\paper 1\\fixed fully\\Cramers V 126.jpg', 
                        format='jpg', bbox_inches='tight', dpi=1200)

        plt.show()
    if return_results:
        return corr



def Theils_significant_above_threshold(corr, threshold=0.5):
    """
    corr from associations above.

    """
    # for the 126 ground truth unmerged cases pruned:

    for semio1 in list(corr.columns):   # semio 1 is the given
        for semio2 in list(corr.columns):
            if (semio1 != semio2) &(corr[semio1][semio2] >threshold):
                print ("("+semio2,"|", semio1+")",corr[semio1][semio2])