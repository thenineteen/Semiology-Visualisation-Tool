import pandas as pd
import numpy as np
from scipy.stats import fisher_exact, chi2_contingency


def multiple_chi2_from_DataFrame(X, y, interaction=[], threshold=0.05):
    """
    as BELOW but chi-squared tests (not fisher) for more than 2x2 tables.
    """

    print('X shape: ', X.shape)
    print('y shape: ', y.shape)
    print()

    #initialise dataframe for copy/paste
    columnss = ['Semiology', 'Odds Ratio', '# with feature and outcome present', 
                        'Total # with this feature', 'p-value']
    significant_univariate_features_df = pd.DataFrame([], columns = columnss)

    # cycle through all features and do fishers exact for all 
    for semio in X.columns:

        Semio_index = X.loc[X[semio]==1, :].index

        freqq_y1 = (X.loc[X[semio]==1, y.name]).sum()
        freqq_y0 = ((X.loc[X[semio]==1, y.name]).count()) - ((X.loc[X[semio]==1, y.name]).sum())
        
        absentsemio_y1 = ((X.loc[X[semio]==0, y.name]).sum())                                 
        absentsemio_y0 = ((X.loc[X[semio]==0, y.name]).count())-((X.loc[X[semio]==0, y.name]).sum())
                
                                                            
        # freq of t Lx in this data, # pts, freq of Other
        total_target = y.sum()
        pts = y.shape[0]  # == y.count()
        other = pts-total_target
        
    # chi2_contingency
        if not interaction:
            chi2, pV, dof, expected = chi2_contingency(np.array([
                [freqq_y1, freqq_y0],
                [absentsemio_y1, absentsemio_y0]
            ]))  # two-sded by default

            oddsR = (freqq_y1/freqq_y0)/((absentsemio_y1)/(absentsemio_y0))

            if pV < (threshold/(len(X.columns))):
                print('\n***Fisher at alpha threshold corrected for mulitiple comparisons: '+str(threshold/(len(X.columns))), '\n',
                    semio, '\n', 
                    'feature present: ', freqq_y1,',', freqq_y0, '\n',
                    'feature absent: ', absentsemio_y1,',', absentsemio_y0, '\n',
                    'OR: ', oddsR, 'p', round(pV,15))



            elif pV < (threshold):
                print('\nFisher at alpha threshold: '+str(threshold), '\n',
                    semio, '\n',
                    'feature present: ', freqq_y1,',', freqq_y0, '\n',
                    'feature absent: ', absentsemio_y1,',', absentsemio_y0, '\n',
                    'OR: ', oddsR, '\n', 
                    'p=', round(pV,15))


            # significant_univariate_features_df.loc[semio, 'Semiology'] = semio
            # significant_univariate_features_df.loc[semio, 'Odds Ratio'] = oddsR
            # significant_univariate_features_df.loc[semio, '# with feature and outcome present'] = freqq_y1   
            # significant_univariate_features_df.loc[semio, 'Total # with this feature'] = freqq_y1 + freqq_y0
            # significant_univariate_features_df.loc[semio, 'p-value'] = round(pV,15)


        if interaction:
            for i in interaction:

                f1_i1_y1 = (X.loc[((X[semio]==1)&(X[i]==1)), y.name]).sum()
                f1_i1_y0 = (X.loc[((X[semio]==1)&(X[i]==1)), y.name]).count() - (X.loc[((X[semio]==1)&(X[i]==1)), y.name]).sum()

                f1_i0_y1 = (X.loc[((X[semio]==1)&(X[i]==0)), y.name]).sum()
                f1_i0_y0 = (X.loc[((X[semio]==1)&(X[i]==0)), y.name]).count() - (X.loc[((X[semio]==1)&(X[i]==0)), y.name]).sum()

                f0_i1_y1 = (X.loc[((X[semio]==0)&(X[i]==1)), y.name]).sum()
                f0_i1_y0 = (X.loc[((X[semio]==0)&(X[i]==1)), y.name]).count() - (X.loc[((X[semio]==0)&(X[i]==1)), y.name]).sum()

                f0_i0_y1 = (X.loc[((X[semio]==0)&(X[i]==0)), y.name]).sum()
                f0_i0_y0 = (X.loc[((X[semio]==0)&(X[i]==0)), y.name]).count() - (X.loc[((X[semio]==0)&(X[i]==0)), y.name]).sum()

                chi2, pV, dof, expected = chi2_contingency(np.array([                        
                    [[f1_i1_y1, f1_i1_y0],
                    [f1_i0_y1, f1_i0_y0]],
                    [[f0_i1_y1, f0_i1_y0],
                    [f0_i0_y1, f0_i0_y0]]
                ]))  # two-sded by default

                if pV < (threshold/(len(X.columns))):
                    print('\n***Chi-2 at alpha threshold corrected for mulitiple comparisons: '+str(threshold/(len(X.columns))), '\n',
                        semio, '\n', 
                        'feature & interaction present: ', f1_i1_y1,',', f1_i1_y0, '\n',
                        'feature present (i absent): ', f1_i0_y1,',', f1_i0_y0, '\n',
                        'feature absent (i present): ', f0_i1_y1, ',', f0_i1_y0, '\n',
                        'feature absent (i absent): ', f0_i0_y1, ',', f0_i0_y0, '\n',
                        'OR: N/A', 'p', round(pV,15))



                elif pV < (threshold):
                    print('\nFisher at alpha threshold: '+str(threshold), '\n',
                        semio, '\n', 
                        'feature & interaction present: ', f1_i1_y1,',', f1_i1_y0, '\n',
                        'feature present (i absent): ', f1_i0_y1,',', f1_i0_y0, '\n',
                        'feature absent (i present): ', f0_i1_y1, ',', f0_i1_y0, '\n',
                        'feature absent (i absent): ', f0_i0_y1, ',', f0_i0_y0, '\n',
                        'OR: N/A', 'p', round(pV,15))


                # significant_univariate_features_df.loc[(semio, interaction), 'Semiology'] = semio
                # significant_univariate_features_df.loc[(semio, interaction), 'Odds Ratio'] = oddsR
                # significant_univariate_features_df.loc[(semio, interaction), '# with feature and outcome present'] = freqq_y1   
                # significant_univariate_features_df.loc[(semio, interaction), 'Total # with this feature'] = freqq_y1 + freqq_y0
                # significant_univariate_features_df.loc[(semio, interaction), 'p-value'] = round(pV,15)



    return significant_univariate_features_df














def multiple_fisher_from_DataFrame(X, y, threshold=0.05):
    """
    Multiple Fisher's tests from a DataFrame. 
    give it the target and predictors. (binary). Ensure X includes the target column (y).
    Manually determine if you want only the training data or entire data set etc
    Manually give it merged or native features


    Marvasti 2019 Dec
    """

    print('X shape: ', X.shape)
    print('y shape: ', y.shape)
    print()

    #initialise dataframe for copy/paste
    columnss = ['Semiology', 'Odds Ratio', '# with feature and outcome present', 
                        'Total # with this feature', 'p-value']
    significant_univariate_features_df = pd.DataFrame([], columns = columnss)

    # cycle through all features and do fishers exact for all 
    for semio in X.columns:

        Semio_index = X.loc[X[semio]==1, :].index

        freqq_y1 = (X.loc[X[semio]==1, y.name]).sum()
        freqq_y0 = ((X.loc[X[semio]==1, y.name]).count()) - ((X.loc[X[semio]==1, y.name]).sum())
        
        absentsemio_y1 = ((X.loc[X[semio]==0, y.name]).sum())                                 
        absentsemio_y0 = ((X.loc[X[semio]==0, y.name]).count())-((X.loc[X[semio]==0, y.name]).sum())
                
                                                            
        # freq of t Lx in this data, # pts, freq of Other
        total_target = y.sum()
        pts = y.shape[0]  # == y.count()
        other = pts-total_target
        
    # Fisher no 2

        oddsR, pV = fisher_exact(np.array([
            [freqq_y1, freqq_y0],
            [absentsemio_y1, absentsemio_y0]
        ]))  # two-sded by default

        if pV < (threshold/(len(X.columns))):
            print('\n***Fisher at alpha threshold corrected for mulitiple comparisons: '+str(threshold/(len(X.columns))), '\n',
                semio, '\n', 
                'feature present: ', freqq_y1,',', freqq_y0, '\n',
                'feature absent: ', absentsemio_y1,',', absentsemio_y0, '\n',
                'OR: ', oddsR, 'p', round(pV,15))



        elif pV < (threshold):
            print('\nFisher at alpha threshold: '+str(threshold), '\n',
                semio, '\n',
                'feature present: ', freqq_y1,',', freqq_y0, '\n',
                'feature absent: ', absentsemio_y1,',', absentsemio_y0, '\n',
                'OR: ', oddsR, '\n', 
                'p=', round(pV,15))


        significant_univariate_features_df.loc[semio, 'Semiology'] = semio
        significant_univariate_features_df.loc[semio, 'Odds Ratio'] = oddsR
        significant_univariate_features_df.loc[semio, '# with feature and outcome present'] = freqq_y1   
        significant_univariate_features_df.loc[semio, 'Total # with this feature'] = freqq_y1 + freqq_y0
        significant_univariate_features_df.loc[semio, 'p-value'] = round(pV,15)

    return significant_univariate_features_df