# 1. convert the localising numbers in pivot_result to 0-100 parcellation intensities:

from sklearn.preprocessing import QuantileTransformer
import seaborn as sns
from scipy.stats import skewnorm, chi2

def pivot_result_to_pixel_intensities(pivot_result, df, 
                                      method='linear', scale_factor=0.6,
                                      use_main_df_calibration=False):
    """
    EpiNav(R) requirement is for pixel intensities to be between 0-100.
    This will conver the pt #s in the localisation to pixel intensities. 
    
    100 max will be taken as the max number of pts in any single localisation.
    0 will be np.nan/ zero
    
    
    ---
    Arguments:
    pivot_result is the final DataFrame output of a specific query.
    df is the overall mega analysis DataFrame required for calibrating the max 100 intensity if use_main_df_calibration==True.
        otherwise, pivot_result itself will be used for calibration.
    method is linear by default. Can use sklearn.preprocessing transform instead to 'normal': quantiletransformer
    scale_factor scales by default value to allow for:
            pixels to increase in intensity from overlapping EpiNav parcellations.
            default is 10 for non-linear quantiletransformer
            deafult is 0.6 for linear
            
    Ali Alim-Marvasti Aug 2019
    """
    
    # checks:
    if pivot_result.shape[0] > 1:
        print('CAN NOT PROCEED: pivot_result has more than one row after pivoting - please check and try again')
        return
    print('Check distribution of pivot_results and its skewnormal transformation:')
    f, axes = plt.subplots(1, 3, figsize=(15,5)) 
    a = sns.distplot(pivot_result, fit=skewnorm, kde=True, ax=axes[0])
    a.set_title('pivot_result skewnorm')
    a.set(xlabel='# pts', ylabel='proportion')

    data = skewnorm.rvs(pivot_result)
    b = sns.distplot(data, fit=skewnorm, kde=False, ax=axes[1])
    b.set_title('skewnorm.rvs pivot_result')
    b.set(xlabel='skewnorm rvs transformation')
    
    
    
    # find the maximal value
    if use_main_df_calibration==True:
        localisation_labels = df.columns[17:72]
        max_value = df[localisation_labels].sum().max()  # usually this is the temporal lobe sum
        mean = df[localisation_labels].sum().mean()
        median = df[localisation_labels].sum().median()
        std = df[localisation_labels].sum().std()
        
        print('Main df and its skewnormal transformation:')
        f, axes = plt.subplots(1, 2) 
        c = sns.distplot(df[localisation_labels].sum(), fit=skewnorm, kde=True, ax=axes[0])
        c.set_title('entire df skewnorm')
        c.set(xlabel='# pts', ylabel='proportion')

        data2 = skewnorm.rvs(df[localisation_labels].sum()) 
        d = sns.distplot(data2, fit=skewnorm, kde=False )
        d.set_title('skewnorm.rvs entire df')
        d.set(xlabel='skewnorm rvs transformation')
        plt.show()
        
        
    elif use_main_df_calibration==False:
        max_value = pivot_result.sum().max()  # usually this is the temporal lobe sum
        mean = pivot_result.sum().mean()
        median = pivot_result.sum().median()
        std = pivot_result.sum().std()
        
    # initialise empty dataframe with same dimensions as target
    pivot_result_intensities = pd.DataFrame().reindex_like(pivot_result)
    
    # linear
    if method=='linear':
        print('Using simple linear transformation, with scale_factor: ', scale_factor)
        for col in pivot_result_intensities:  # col names are the same
            normalised_max = ( (pivot_result.loc[:, col] - mean)/max_value )
            normalsied_std = ( (pivot_result.loc[:, col] - mean)/std )
            pivot_result_intensities.loc[:, col] = scale_factor*round( normalised_max*100 )
#             pivot_result_intensities.loc[:, col] = scale_factor*round( normalsied_std )


    
    elif method != 'linear':
        method = 'QuantileTransformer'
        scale_factor = 10
        print('Using sklearn.preprocessing QuantileTransformer, with scale_factor: ', scale_factor)

        QT = QuantileTransformer(n_quantiles=10,
                                output_distribution='normal',
                                   )
        
        QT_array = QT.fit_transform(pivot_result.values.reshape(-1,1))
        
        n = 0
        for col in pivot_result_intensities:  # col names are the same
            pivot_result_intensities.loc[:, col] = 10*QT_array[n]
            n +=1
                
    
    # plot chosen transformation
    data = pivot_result_intensities
    c = sns.distplot(data, fit=norm, kde=False, ax=axes[2])
    titre = 'Your chosen tranform of pivot_result: ' + str(method)
    c.set_title(titre)
    xlabeltitre = '# pts '+str(method)+' * '+ str(scale_factor)
    c.set(xlabel=xlabeltitre)
    plt.show()
    
    
    # get rid of negative values
    print_counter = 0
    for col in range(0, len(pivot_result_intensities.columns)-1):
        if pivot_result_intensities.iloc[0, col] < 0:
            pivot_result_intensities.iloc[0, col] = 0

            if print_counter == 0: 
                print('All negative values floored to zero for EpiNav')
                print_counter = 1
        if pivot_result_intensities.iloc[0, col] > 70:
            print('Intensity might saturate as ', col, 'on its own has over 70 intensity value')
    
    pivot_result_intensities.index.name = 'intensities (0-100)'
    return pivot_result_intensities

    

    