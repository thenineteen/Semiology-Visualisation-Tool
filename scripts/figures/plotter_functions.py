import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.transforms import Affine2D

def plot_proportion_ci_forest_plot(proportion_df_1,
                                   confint_df_1,
                                   counts_df_1,
                                   colors,
                                   plotter_settings,
                                   legend_labels,
                                   proportion_df_2,
                                   confint_df_2,
                                   counts_df_2,
                                   y_labels = None,
                                   overlapping = False,
                                   ax_titles = None,
                                  ):
    n_rows, n_columns =  proportion_df_1.shape
    subplot_width = int(n_rows / 3) + (n_rows % 3 > 0) # axes are in 3 rows, subplot_width columns
    
    fig, axs = plt.subplots(subplot_width, 3, sharex=True, sharey=True, figsize=(7, 8))
    
    if not y_labels:
        y_labels = proportion_df_1.columns

    for i, row_name in enumerate(proportion_df_1.index):
        # Plot on one axis at a time
        coord = divmod(i, 3)
        ax = axs[coord[0], coord[1]]
    
        if not overlapping and proportion_df_2 is not None:
            trans1 = Affine2D().translate(0, -0.21) + ax.transData
            trans2 = Affine2D().translate(0, +0.21) + ax.transData
            transforms = [trans1, trans2]
        else:
            transforms = [None, None]
        
        # Plot first data points (potentially one of two)
        x = proportion_df_1.loc[row_name]
        xerr = np.array([confint_df_1[0].loc[row_name].values, confint_df_1[1].loc[row_name].values])
        ax.errorbar(x,
                    y_labels,
                    xerr = xerr,
                    color = colors[0],
                    label = legend_labels[0],
                    transform = transforms[0],
                    markerfacecolor = 'white',
                    **plotter_settings)
        
        total_row_1 = int(counts_df_1.loc[row_name].sum())
        n_label_text = f' (n = {total_row_1}'
        
        # Plot second set of datapoints (usually second colour, might be SS only)
        if proportion_df_2 is not None:
            x = proportion_df_2.loc[row_name]
            xerr = np.array([confint_df_2[0].loc[row_name].values, confint_df_2[1].loc[row_name].values])
            ax.errorbar(x,
                    y_labels,
                    xerr = xerr,
#                     color = colors[1], #comment out for default blue
                    label = legend_labels[1],
                    transform = transforms[1],
                    **plotter_settings)
            
            total_row_2 = int(counts_df_2.loc[row_name].sum())
            n_label_text += f', {total_row_2}'
        
        
        try:
            ax.title.set_text(ax_titles[i] + n_label_text + ')')
        except TypeError:
            ax.title.set_text(row_name + n_label_text + ')')
            
        ax.set_xlim([-0.05,1])
        plt.xticks(np.arange(0, 1.1, 0.2))
        ax.axvline(x=1/len(x),ymin=0,ymax=1,c='darkgray', linewidth=1, zorder=0, clip_on=False)
    
    ax.invert_yaxis()

    axs[subplot_width-1, 1].set_xlabel('P (Localisation | Semiology)', ha='center')
    plt.tight_layout()


def clean_labels(labels):
    pre_localisation = ['Anterior (temporal pole)',
             'Lateral Temporal',
             'Mesial Temporal',
             'Posterior Temporal',
             'Basal (including Fusiform OTMG)',
             'Hypothalamus',
             'PL',
             'CING',
             'OL',
             'FL',
             'INSULA',
             'All other']

    post_localisation = ['Anterior Temporal',
     'Lateral Temporal',
     'Mesial Temporal',
     'Posterior Temporal',
     'Basal Temporal',
     'Hypothalamus',
     'Parietal Lobe',
     'Cingulate Gyrus',
     'Occipital Lobe',
     'Frontal Lobe',
     'Insula',
     'Interlobar Junctions+']
    
    pre_semiology = ['Epigastric', 'Fear-Anxiety', 'Psychic', 'Autonomous-Vegetative',
       'Olfactory', 'Visual - Elementary', 'Somatosensory',
       'Non-Specific Aura', 'Head or Body Turn', 'Head Version', 'Tonic',
       'Dystonic', 'Clonic', 'Hypermotor', 'Complex Behavioural',
       'Automatisms Combination - Manual LowerLimb Oral',
       'Vocalisation: Unintelligible Noises', 'Aphasia',
       'Ictal Speech: Formed Words', 'Dialeptic/LOA']
    
    post_semiology = ['Epigastric', 'Fear-Anxiety', 'Psychic', 'Autonomic',
       'Olfactory', 'Visual - Elementary', 'Somatosensory',
       'Non-Specific Aura', 'Head or Body Turn', 'Head Version', 'Tonic',
       'Dystonic', 'Clonic', 'Hypermotor', 'Complex Behavioural',
       'Automatisms','Unintelligible Noises', 'Aphasia',
       'Ictal Speech: Formed Words', 'Dialeptic/LOA']

    look_up_dict = dict(zip(pre_localisation+pre_semiology, post_localisation+post_semiology))

    return [look_up_dict[label] for label in labels]