import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.transforms import Affine2D


def plot_proportion_ci_forest_plot(proportion_df_1,
                                   confint_df_1,
                                   counts_df_1,
                                   colors,
                                   legend_labels,
                                   proportion_df_2,
                                   confint_df_2,
                                   counts_df_2,
                                   y_labels=None,
                                   overlapping=False,
                                   ax_titles=None,
                                   xlim=[-0.05, 1],
                                   xticks=np.arange(0, 1.1, 0.2),
                                   vline='proportion',
                                   xlabel='P (Localisation | Semiology)',
                                   figsize=(7, 8),
                                   plotter_settings=None,
                                   localising_n=None, fontsize=8,
                                   ):
    """
    Plot a forest plot of proportions and confidence intervals. Can be two sets of data points
    (different colours) on each axis.

    If only one set of points, set proportion_df_2, confint_df_2, counts_df_2 = None

    localising_n = query_results from figures.ipynb
    """
    n_rows, n_columns = proportion_df_1.shape
    # axes are in 3 rows, subplot_width columns
    subplot_width = int(n_rows / 3) + (n_rows % 3 > 0)

    fig, axs = plt.subplots(subplot_width, 3, sharex=True,
                            sharey=True, figsize=figsize)

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
        xerr = np.array([confint_df_1[0].loc[row_name].values,
                         confint_df_1[1].loc[row_name].values])
        ax.errorbar(x,
                    y_labels,
                    xerr=xerr,
                    color=colors[0],
                    label=legend_labels[0],
                    transform=transforms[0],
                    markerfacecolor='white',
                    **plotter_settings)

        total_row_1 = int(counts_df_1.loc[row_name].sum())
        n_label_text = f' (N = {total_row_1}'

        # Plot second set of datapoints (usually second colour, might be SS only)
        if proportion_df_2 is not None:
            x = proportion_df_2.loc[row_name]
            xerr = np.array([confint_df_2[0].loc[row_name].values,
                             confint_df_2[1].loc[row_name].values])
            ax.errorbar(x,
                        y_labels,
                        xerr=xerr,
                        #                     color = colors[1], #comment out for default blue
                        label=legend_labels[1],
                        transform=transforms[1],
                        **plotter_settings)

            total_row_2 = int(counts_df_2.loc[row_name].sum())
            n_label_text += f', {total_row_2}'
            if localising_n:
                txt1 = str(int(localising_n['full']
                               [row_name]['num_query_loc']))
                n_label_text += f'; n = {txt1}'
                txt2 = str(
                    int(localising_n['spontaneous'][row_name]['num_query_loc']))
                n_label_text += f', {txt2}'

        if not localising_n:
            try:
                ax.title.set_text(ax_titles[i] + n_label_text + ')')
            except TypeError:
                ax.title.set_text(row_name + n_label_text + ')')
        elif localising_n:
            ax.set_title(row_name + n_label_text + ')',
                         fontdict={'fontsize': fontsize})

        ax.set_xlim(xlim)
        plt.xticks(xticks)
        if vline == 'proportion':
            ax.axvline(x=1/len(x), ymin=0, ymax=1, c='darkgray',
                       linewidth=1, zorder=0, clip_on=False)
        else:
            ax.axvline(x=vline, ymin=0, ymax=1, c='darkgray',
                       linewidth=1, zorder=0, clip_on=False)

    ax.invert_yaxis()

    axs[subplot_width-1, 1].set_xlabel(xlabel, ha='center')
    plt.tight_layout()

    return fig, axs


def plot_stacked_hbar(proportions_df, ax, ax_title=None, axis='semiology', y_labels=None, color_palette=sns.color_palette("Paired", 12)):
    if y_labels is not None:
        proportions_df.columns = y_labels

    if axis == 'semiology':
        proportions_df = proportions_df
        xlabel = 'P(Localisation | Semiology)'
    elif axis == 'zone':
        proportions_df = proportions_df.T
        xlabel = 'P(Semiology | Localisation)'
    else:
        raise ValueError('axis kwarg must be from {semiology, zone}')

    proportions_df[::-1].plot(kind='barh', colormap=color_palette,
                              stacked=True, figsize=(10, 4), ax=ax)
    plt.gca().set_xlim((0, 1))

    ax.title.set_text(ax_title)
    ax.set_xlabel(xlabel)
