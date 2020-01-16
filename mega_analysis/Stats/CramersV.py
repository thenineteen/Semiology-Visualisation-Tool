from scipy.stats import chi2_contingency
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


def cramers_corrected_stat(confusion_matrix):
    """ calculate Cramers V statistic for categorial-categorial association.
        uses correction from Bergsma and Wicher, 
        Journal of the Korean Statistical Society 42 (2013): 323-328
    """    

    chi2 = chi2_contingency(confusion_matrix)[0]
    n = confusion_matrix.sum().sum()
    phi2 = chi2/n
    r,k = confusion_matrix.shape
    phi2corr = max(0, phi2 - ((k-1)*(r-1))/(n-1))    
    rcorr = r - ((r-1)**2)/(n-1)
    kcorr = k - ((k-1)**2)/(n-1)
    return np.sqrt(phi2corr / min( (kcorr-1), (rcorr-1)))


def cramers_corr_multiple(X, m, n):
    """
    compares one feature m with another n
    """
    confusion_matrix = pd.crosstab(X.iloc[:,m], X.iloc[:,n])
#     print(X.columns[m], 'and', X.columns[n])
    ans = cramers_corrected_stat(confusion_matrix)
    return ans


def all_cramers(X):
    """
    compares all cramers pair-wise and plots
    """
    ans = []
    
    for m in range (0, X.shape[1]):
        for n in range (0, X.shape[1]):
#             ans = np.append(ans, cramers_corr_multiple(X, m, n), axis=0)
#             np.column_stack((ans, cramers_corr_multiple(X, m, n)))
            ans.append(cramers_corr_multiple(X, m, n))
    return ans


def CramersV(X, 
            title='Categorical Correlation: Cramer\'s V \n309 Patients, 43 Semiologies',
            savefigure=False):

    ans = all_cramers(X)
    ansdf = pd.DataFrame(ans)

    plt.figure()
    sns.heatmap(ansdf, annot=False, fmt='fnt', cmap='YlOrRd')
    plt.title(title)
    plt.xticks(np.arange(X.shape[1]), X.columns, rotation='vertical', fontsize=6, fontweight='ultralight')
    plt.yticks(np.arange(X.shape[1]), X.columns, fontsize=6)
    
    if savefigure:
        plt.savefig('L:\\word_docs\\NLP\\Data Pickles\\automated\\updated dataframes\\CramersV_change_the_name.eps', 
                        format='eps', bbox_inches='tight', dpi=1200)
    plt.show()