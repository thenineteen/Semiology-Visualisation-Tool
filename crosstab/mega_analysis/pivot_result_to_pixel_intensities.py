# 1. convert the localising numbers in pivot_result to 0-100 parcellation intensities:

from sklearn.preprocessing import QuantileTransformer, MinMaxScaler
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import skewnorm, chi2, norm
import scipy.stats


def use_df_to_transform_pivot_result(df_or_pivot_result, pivot_result, quantiles, scale_factor):
    """
    instead of using query subset of data, use entire df for fitting quantile transformer.
    Then transform the query subset data.
    Called by pivot_result_to_pixel_intensities
    Ali Alim-Marvasti Aug 2019

    """
    pivot_result_intensities = pd.DataFrame().reindex_like(pivot_result)
    method = 'QuantileTransformer'
    scale_factor = scale_factor
    print('Using QuantileTransformer in use_df_to_transform_pivot_result, with scale_factor: ', scale_factor)

    QT = QuantileTransformer(n_quantiles=quantiles, output_distribution='normal')
    QT.fit(df_or_pivot_result.values.reshape(-1,1))
    QT_array = QT.transform(pivot_result.values.reshape(-1,1))
    
    n = 0
    for col in pivot_result_intensities:  # col names are the same
        pivot_result_intensities.loc[:, col] = 10*QT_array[n]
        n +=1
            
    return pivot_result_intensities




def intensities_factor(df_or_pivot_result, quantiles=10,
                      method='non-linear', scale_factor=10
                      ):
    """
    normalises values in pivot_result_intensities to between 0-100 for EpiNav visualisation,
    using either the entire df or pivot_result subset.
    
    Called by pivot_result_to_pixel_intensities. 
    Currently this is called appropriately when using lateralisation.
    If ignoring lateralisation and using it as part of a symmetric localisation pipeline subsequent to 
        QUEREY_SEMIOLOGY or QUERY_INTERSECTION, then it is problematic: it looks at the distribution of the regions before gif parcellations. 
    Ali Alim-Marvasti Aug 2019
    """
    
    # initialise empty dataframe with same dimensions as target: 
    pivot_result_intensities = pd.DataFrame().reindex_like(df_or_pivot_result)

        
    #linear 
    if method == 'linear':
        
        scale_factor = 0.6
        max_value = df_or_pivot_result.sum().max()  # usually this is the temporal lobe sum
        mean = df_or_pivot_result.sum().mean()
        median = df_or_pivot_result.sum().median()
        std = df_or_pivot_result.sum().std()
        print('Using simple linear transformation, with scale_factor: ', scale_factor)
        
        for col in pivot_result_intensities:  # col names are the same
            normalised_max = ( (df_or_pivot_result.loc[:, col] - mean)/max_value )
           #  normalsied_std = ( (df_or_pivot_result.loc[:, col] - mean)/std )
            pivot_result_intensities.loc[:, col] = scale_factor*round( normalised_max*100 )
           #  pivot_result_intensities.loc[:, col] = scale_factor*round( normalsied_std )

    
    elif (method == 'non-linear')|(method == 'nonlinear'):
        
        method = 'QuantileTransformer'
        scale_factor = scale_factor
        print('Using sklearn.preprocessing QuantileTransformer, with scale_factor: ', scale_factor)

        QT = QuantileTransformer(n_quantiles=quantiles, output_distribution='normal')
        QT_array = QT.fit_transform(df_or_pivot_result.values.reshape(-1,1))
        # n = 0
        # for col in pivot_result_intensities:  # col names are the same
        #     pivot_result_intensities.loc[:, col] = scale_factor * QT_array[n]
        #     n +=1
        # new way to do it faster than above iterating:
        QT_array = QT_array.reshape(-1,)
        pivot_result_intensities.iloc[0, :] = scale_factor * QT_array

    elif method == 'min_max':
        print('Using sklearn.preprocessing MinMaxScaler')
        scaler = MinMaxScaler(feature_range=(1,100))
        minmax_array = scaler.fit_transform(df_or_pivot_result.values.reshape(-1,1))
        minmax_array = minmax_array.reshape(-1,)
        pivot_result_intensities.iloc[0, :] = minmax_array

    elif method == 'chi2':  # doesn't work yet
        # https://stackoverflow.com/questions/6620471/fitting-empirical-distribution-to-theoretical-ones-with-scipy-python
        dist_names = ['chi2']
        for dist_name in dist_names:
            dist = getattr(scipy.stats, dist_name)
            chi_squared_dist = dist.fit_transform(df_or_pivot_result.values.reshape(-1,1))
            pivot_result_intensities.iloc[0, :] = chi_squared_dist

    return pivot_result_intensities
    
    
    
    

def pivot_result_to_pixel_intensities(pivot_result, df, 
                                      method='non-linear', scale_factor=10, quantiles=10,
                                      use_main_df_calibration=False):
    """
    EpiNav(R) requirement is for pixel intensities to be between 0-100.
    This will conver the pt #s in the localisation to pixel intensities. 

    pivot_result is from melt_then_pivot_query
    
    100 max will be taken as the max number of pts in any single localisation.
    0 will be np.nan/ zero
    
    
    ---
    Arguments:
    pivot_result is the final DataFrame output of a specific query (melt_then_pivot_query).
    df is the overall mega analysis DataFrame required for calibrating the max 100 intensity if use_main_df_calibration==True.
        otherwise, pivot_result itself will be used for calibration.
    method is 'non-linear' by default: uses sklearn.preprocessing.quantiletransformer 'normal'
        Can instead be set to 'linear'. Uses max value to standardise. 
    scale_factor scales by default value to allow for:
            pixels to increase in intensity from overlapping EpiNav parcellations.
            default is 10 for non-linear quantiletransformer
            deafult is 0.6 for linear
            
    Ali Alim-Marvasti Aug 2019
    """
    # default colour and extra string for titles:
    color = 'b'
    color_df = 'b'
    extra_title_df = ''
    extra_title_pivot = ''
    now_transform_pivot_result_using_QT_from_df = False

    # checks:
    if pivot_result.shape[0] > 1:   
        if 'pt #s' in pivot_result.columns:
            print('It seems instead of pivot_result we are using all_combined_gifs DataFrame from...')
            print('...QUERY_LATERALISATION. In which case, use all_combined_gifs[[\'pt #s\']].T as arg for pivot_result')
            print('Or better, use query_lateralisation_to_pixel_intensities from laterlised_intensities.')
            return
        else:
            print('CAN NOT PROCEED: pivot_result has more than one row after pivoting - please check and try again')
            return
    
    # look at distribution of pivot_result
    print('Check distribution of pivot_results, skewnormal & transformation:')
    fig, axes = plt.subplots(2, 3, figsize=(15,5)) 
    a = sns.distplot(pivot_result, fit=skewnorm, kde=True, ax=axes[0, 0])
    a.set_title('pivot_result skewnorm')
    a.set(xlabel='pt #s', ylabel='proportion')

    data = skewnorm.rvs(pivot_result)
    b = sns.distplot(data, fit=skewnorm, kde=False, ax=axes[0, 1])
    b.set_title('skewnorm.rvs pivot_result')
    b.set(xlabel='skewnorm rvs transformation')
    
    
    # look at distribution of df: use the entire df distribution of frequency of #s of pts
    localisation_labels = df.columns[17:72]
    max_value = df[localisation_labels].sum().max()  # usually this is the temporal lobe sum
    mean = df[localisation_labels].sum().mean()
    median = df[localisation_labels].sum().median()
    std = df[localisation_labels].sum().std()

    print('Main df, skewnormal & transformation:')
    c = sns.distplot(df[localisation_labels].sum(), fit=skewnorm, kde=True, ax=axes[1,0])
    c.set_title('entire df skewnorm')
    c.set(xlabel='pt #s', ylabel='proportion')

    data2 = skewnorm.rvs(df[localisation_labels].sum()) 
    d = sns.distplot(data2, fit=skewnorm, kde=False, ax=axes[1,1] )
    d.set_title('skewnorm.rvs entire df')
    d.set(xlabel='skewnorm rvs transformation')


    # run the tranformation with df:
    if use_main_df_calibration==True:
#         df_or_pivot_result = df[localisation_labels].sum() # actually needs to be considerably more nuanced to work:
        df_or_pivot_result = pd.DataFrame(df[localisation_labels].sum(axis='rows')).T.sort_values(by = 0, axis=1, inplace=False, ascending=False)
        color_df = 'r'
        extra_title_df = 'Chosen '
        now_transform_pivot_result_using_QT_from_df = True

    # plot the QuantileTransformed entire df:
    #innitialise the entire df
    df_or_pivot_result = pd.DataFrame(df[localisation_labels].sum(axis='rows')).T.sort_values(by = 0, axis=1, inplace=False, ascending=False)
    pivot_result_intensities = intensities_factor(df_or_pivot_result, quantiles, method=method, scale_factor=scale_factor)
    # plot df
    df_or_pivot_str = 'entire DataFrame: '
    data = pivot_result_intensities
    e = sns.distplot(data, fit=norm, kde=False, ax=axes[1,2], color=color_df)
    titre = extra_title_df +'Transform of '+ str(df_or_pivot_str) + str(method)
    e.set_title(titre)
    xlabeltitre = 'pt #s '+str(method)+' * '+ str(scale_factor)
    e.set(xlabel=xlabeltitre)
    

    # use pivot_result instead of df:
    if use_main_df_calibration==False:
        df_or_pivot_result = pivot_result
        extra_title_pivot = 'Chosen '
        color = 'r'
    #plot
    df_or_pivot_result = pivot_result
    pivot_result_intensities = intensities_factor(df_or_pivot_result, quantiles, method=method, scale_factor=scale_factor)
    # plot pivot_result transformation
    df_or_pivot_str = 'pivot_result: '
    data = pivot_result_intensities
    e = sns.distplot(data, fit=norm, kde=False, ax=axes[0,2], color=color)
    titre = extra_title_pivot+'Transform of '+ str(df_or_pivot_str) + str(method)
    e.set_title(titre)
    xlabeltitre = 'pt #s '+str(method)+' * '+ str(scale_factor)
    e.set(xlabel=xlabeltitre)

    fig.tight_layout()
    plt.show()

    # after all the plotting, use the fitted QT to transform the data:
    if now_transform_pivot_result_using_QT_from_df:
        df_or_pivot_result = pd.DataFrame(df[localisation_labels].sum(axis='rows')).T.sort_values(by = 0, axis=1, inplace=False, ascending=False)
        pivot_result_intensities = use_df_to_transform_pivot_result(df_or_pivot_result, pivot_result, quantiles, scale_factor)

    
    # get rid of negative values
    print_counter = 0
    for col in range(0, len(pivot_result_intensities.columns)):
        if pivot_result_intensities.iloc[0, col] < 0:
            pivot_result_intensities.iloc[0, col] = 0
            if print_counter == 0: 
                print('All negative values floored to zero for EpiNav')
                print_counter = 1
        if pivot_result_intensities.iloc[0, col] > 55:
            print('Intensity might saturate as ', col, 'on its own has intensity value:', pivot_result_intensities.iloc[0, col])
    
    pivot_result_intensities.index.name = 'intensities (0-100)'
    return pivot_result_intensities.round()

    

    
    