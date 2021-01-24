import numpy as np
import pandas as pd
import random

def bootstrap_frequency_array(counts, n_samples=1000, alpha = 0.05):
    """
        Calculate bootstrapped confidence intervals for a list of frequencies associated with categories
    """

    flat_data = []
    for category, total in enumerate(counts):
        flat_data += [category]*int(total)
        
    sampling_counts = []
    for i in range(n_samples):
        sub_sample = np.random.choice(flat_data, len(flat_data))
        sub_sample_counts = [len(sub_sample[sub_sample == category]) for category, total in enumerate(counts)]
        sampling_counts.append(sub_sample_counts)
    
    lower_limits = []
    upper_limits = []
    for category, total in enumerate(counts):
        category_counts = np.array(sampling_counts)[:, category]
        category_counts.sort()
        lower_limits.append(category_counts[int(len(category_counts)*(alpha/2))])
        upper_limits.append(category_counts[int(len(category_counts)*(1-(alpha/2)))])
        
    return np.array([lower_limits, upper_limits])

def bootstrap_frequency_matrix(counts_df, n_samples=1000, axis='semiology'):
    """
        Calculate bootstrapped confidence intervals for 2 dimensional matrix of 
        categorical frequencies. 2d wrapper for 1d function bootstrap_frequency_array

        (usually pass in counts_df)
    """
    if axis == 'zone':
        counts_df = counts_df.T
    elif axis == 'semiology':
        pass
    else:
        raise ValueError('axis must be given from {semiology, zone}')

    upper_ci_counts = pd.DataFrame(index = counts_df.index, columns = counts_df.columns)
    lower_ci_counts = pd.DataFrame(index = counts_df.index, columns = counts_df.columns)

    for column in counts_df.columns:
        lower_limits, upper_limits = bootstrap_frequency_array(counts_df[column].values, n_samples)
        lower_ci_counts[column] = lower_limits
        upper_ci_counts[column] = upper_limits
        
    lower_ci_proportions = lower_ci_counts.div(counts_df.sum(1), axis='index')
    upper_ci_proportions = upper_ci_counts.div(counts_df.sum(1), axis='index')
    
    return lower_ci_proportions, upper_ci_proportions