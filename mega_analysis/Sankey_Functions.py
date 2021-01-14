import pandas as pd
import numpy as np

import chart_studio.plotly as py
import plotly.io as pio
from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot, init_notebook_mode
import cufflinks as cf
cf.go_offline()
init_notebook_mode()


def flatten_SemioDict(SemioDict, flat_SemioDict_gen={}):
    """    Flattense nested dictionary to low level keys:values. Marvasti Nov 2020    """

    for k, v in SemioDict.items():
        if type(v) is not dict:
            yield {k: v}
            # flat_SemioDict[k] = v
        elif type(v) is dict:
            yield from flatten_SemioDict(v)


def top_level_lobes():
    Lobes = ['TL', 'FL', 'CING', 'PL', 'OL', 'INSULA',
             'Hypothalamus', 'Sub-Callosal Cortex', 'Cerebellum', 'Perisylvian',
             'FT', 'TO', 'TP', 'FTP', 'TPO Junction',
             'PO', 'FP']
    return Lobes


def normalise_top_level_localisation_cols(df):
    """ If the sum of datapoints in lobes is greater than localising col, normalise to localising semiology.
    Akin to Normalise_to_localising value in main mega analysis module, but uses only top level lobes.
    Should not run normalisation methods together """

    Lobes = top_level_lobes()
    df_temp = df.copy()
    df_temp = df_temp[Lobes]

    df_temp.loc[:, 'ratio'] = df['Localising'] / (df[Lobes].sum(axis=1))
    df_temp = df_temp.astype({'ratio': 'float'})

    df.loc[:, Lobes] = (df_temp.loc[:, Lobes]).multiply(
        df_temp.loc[:, 'ratio'], axis=0)

    return df, Lobes


def normalise_top_level_localisation_cols_OTHER(df, *args):
    """
    Compress the localisations to OTHER. Need to have made the OTHER lobe column. Should not run normalisation methods together.
    """
    OTHER = ['Sub-Callosal Cortex', 'TPO Junction', 'TP', 'FTP', 'TO', 'FP', 'Perisylvian',
             'PO', 'FT', 'Cerebellum']

    if 'LobesOTHER_splitTL' not in args:
        LobesOTHER = ['TL', 'FL', 'CING', 'PL', 'OL', 'INSULA',
                      'Hypothalamus', 'OTHER']
    else:
        OTHER = ['Sub-Callosal Cortex', 'TPO Junction', 'TP', 'FTP', 'TO', 'FP', 'Perisylvian',
                 'PO', 'FT', 'Cerebellum']
        LobesOTHER = ['TL', 'FL', 'CING', 'PL', 'OL', 'INSULA',
                      'Hypothalamus', 'OTHER']
        LobesOTHER_splitTL = [i for i in LobesOTHER if i not in ['TL']]
        TL_split = ['Anterior (temporal pole)', 'Lateral Temporal',
                    'Mesial Temporal', 'Posterior Temporal']
        LobesOTHER_splitTL.extend(TL_split)
        LobesOTHER = LobesOTHER_splitTL

    df_temp = df.copy()
    df_temp.loc[:, 'OTHER'] = df_temp[OTHER].sum(axis=1)

    df_temp.loc[:, 'ratio'] = df_temp['Localising'] / \
        (df_temp[LobesOTHER].sum(axis=1))
    df_temp = df_temp.astype({'ratio': 'float'})

    df_temp.loc[:, LobesOTHER] = (df_temp.loc[:, LobesOTHER]).multiply(
        df_temp.loc[:, 'ratio'], axis=0)

    return df_temp, LobesOTHER


def normalise_localisation_cols_OTHER_SplitTL(df, **kwargs):
    """
    Compress the localisations to OTHER but also keep TL split into 4 subregions. Need to have made the OTHER lobe column. Should not run normalisation methods together.
    Note that the hierarchy/postcode data entry (as long as previous normalisation not ran) could result in some TL cases that are not included in the subregions.Distribute these equally.

    THIS WON'T WORK WITHOUT NORMLAISATION TO ALL OTHER LAYERS

    """
    OTHER = ['Sub-Callosal Cortex', 'TPO Junction', 'TP', 'FTP', 'TO', 'FP', 'Perisylvian',
             'PO', 'FT', 'Cerebellum']
    LobesOTHER = ['TL', 'FL', 'CING', 'PL', 'OL', 'INSULA',
                  'Hypothalamus', 'OTHER']
    LobesOTHER_splitTL = [i for i in LobesOTHER if i not in ['TL']]
    TL_split = ['Anterior (temporal pole)', 'Lateral Temporal',
                'Mesial Temporal', 'Posterior Temporal', 'Basal (including Fusiform OTMG)']
    LobesOTHER_splitTL.extend(TL_split)

    df_temp = df.copy()
    df_temp.loc[:, 'OTHER'] = df_temp[OTHER].sum(axis=1)

    if 'normalise_top_level_first' in kwargs:
        # use other function
        df_temp, LobeslOTHER = normaise_top_level_localisation_cols_OTHER(
            df_temp)
        # now normalise TL subregions to TL:
        df_temp.loc[:, 'TL subregion ratio'] = df_temp['TL'] / \
            (df_temp[TL_split].sum(axis=1))
        df_temp = df_temp.astype({'TL subregion ratio': 'float'})
        df_temp.loc[:, TL_split] = (df_temp.loc[:, TL_split]).multiply(
            df_temp.loc[:, 'TL subregion ratio'], axis=0)

    else:
        # distribute excess TL to the 5 subregions equally; i.e. normalise TL_split to TL as we did previously for Localising, taking into account whether TL is greater or less than
        # # only if we want to distribute excess. There will also be some cases where 1 TL localised to both anterior and mesial temporal so we (should!) exclude this mask.
        mask = (df_temp['TL']) > (df_temp[TL_split]).sum(axis=1)
        df_temp['TL subregion ratio'] = 1
        df_temp.loc[mask, 'TL subregion ratio'] = df_temp['TL'] / \
            (df_temp[TL_split].sum(axis=1))
        df_temp = df_temp.astype(
            {'TL subregion ratio': 'float'}, errors='ignore')
        df_temp.loc[:, LobesOTHER_splitTL] = (df_temp.loc[:, LobesOTHER_splitTL]).multiply(
            df_temp.loc[:, 'TL subregion ratio'], axis=0)

        # now go back to do top level normalisation
        df_temp.loc[:, 'ratio'] = df_temp['Localising'] / \
            (df_temp[LobesOTHER_splitTL].sum(axis=1))
        df_temp = df_temp.astype({'ratio': 'float'})
        df_temp.loc[:, LobesOTHER_splitTL] = (df_temp.loc[:, LobesOTHER_splitTL]).multiply(
            df_temp.loc[:, 'ratio'], axis=0)

    return df_temp, LobesOTHER_splitTL


def extract_year_of_publication(df):
    """ EXTRACT YEAR OF PUBLICATION and compress 1954-2000 """

    # check series
    assert type(df['Reference']) == pd.core.series.Series
    # main code: regex for  year of publication
    df['Year'] = df['Reference'].str.extract(r'(?P<Year>\d\d\d\d)')
    df = df.astype({'Year': 'int32'})
    df.loc[df['Year'] < 2001, 'Year'] = '1954-2000'

    return df


def GT_setup1(df):
    """
    Setup the ground truths layer of Sankey. Stored in col called "Labels" in the df.

    """

    postop = 'Post-op Sz Freedom (Engel Ia, Ib; ILAE 1, 2)'
    concordant = 'Concordant Neurophys & Imaging (MRI, PET, SPECT)'
    invEEG = 'sEEG (y) and/or ES (ES)'

    POSTOPS = df[postop].dropna(axis=0, how='any').copy()
    CONCORDANT = df[concordant].dropna(axis=0, how='any').copy()
    INV_EEG = df[invEEG].dropna(axis=0, how='any').copy()

    GT_conditions = [
        (
            (df[postop] == 'y') & (df[concordant].isnull()) & (
                df[invEEG].isnull())
        ),
        (df[postop].isnull()) & (
            df[concordant].notnull()) & (df[invEEG].isnull()),
        ((df[postop].isnull()) & (df[concordant].isnull())
         & (df[invEEG].notnull())),
        ((df[postop] == 'y') & (df[concordant].notnull()) & (df[invEEG].isnull())),
        ((df[postop] == 'y') & (df[concordant].isnull()) & (df[invEEG].notnull())),
        ((df[postop].isnull()) & (df[concordant].notnull())
         & (df[invEEG].notnull())),
        ((df[postop] == 'y') & (df[concordant].notnull()) & (df[invEEG].notnull())),
        # ((df[postop].isnull()) & (df[concordant].isnull()) & (df[invEEG].isnull())),
    ]
    choices = ['Seizure-Freedom Only',
               'Concordance Only',
               'sEEG Only',
               'SF and Concordance',
               'SF and sEEG',
               'Concordance and sEEG',
               'All 3 Ground Truths',
               ]
    Node_Label_df = pd.DataFrame(choices)
    Node_Label_df.columns = ['Node, Label']

    df['Labels'] = np.select(GT_conditions, choices, default='Error')

    # remove errors
    idx = df[
        ((df[postop].isnull()) & (df[concordant].isnull()) & (df[invEEG].isnull()))
    ].index
    df.drop(index=idx, inplace=True)
    df = df[df.Labels != 'Error']

    return df, Node_Label_df


def Priors_setup2(df, Node_Label_df):
    """
    df input is after setup for GT.
    Adds the priors to the Node_Label_df.
    """
    df.loc[df['Spontaneous Semiology (SS)'].notnull(
    ), 'Priors'] = 'Spontaneous Semiology (SS)'
    df.loc[df['Cortical Stimulation (CS)'].notnull(
    ), 'Priors'] = 'Cortical Stimulation (CS)'
    df.loc[df['Epilepsy Topology (ET)'].notnull(),
           'Priors'] = 'Epilepsy Topology (ET)'

    df_groupby = df.groupby(by=['Labels', 'Priors'])[
        'Localising'].sum().to_frame().reset_index()

    priors_df = pd.DataFrame(['Spontaneous Semiology (SS)',
                              'Cortical Stimulation (CS)', 'Epilepsy Topology (ET)'
                              ])
    priors_df.columns = ['Node, Label']

    nodelabel_combined = pd.concat([Node_Label_df, priors_df], axis=0)
    nodelabel_combined = nodelabel_combined.reset_index()
    nodelabel_combined['index'] = nodelabel_combined.index

    sankey_df = pd.concat([df_groupby, nodelabel_combined], axis=1)
    sankey_df = sankey_df.merge(
        nodelabel_combined, left_on='Labels', right_on='Node, Label')
    sankey_df.rename(columns={'number_x': 'Source'})
    sankey_df = sankey_df.merge(
        nodelabel_combined, left_on='Priors', right_on='Node, Label')
    sankey_df.rename(columns={'number_y': 'Target'})
    sankey_df.rename(columns={'index_y': 'Source',
                              'index': 'Target'}, inplace=True)

    return sankey_df, nodelabel_combined


def Sankey_new_layer2(df,
                      layer1,
                      layer2,
                      *args_df,
                      args_list,
                      already_melted='both',  # both layer1 and 2 already melted
                      **kwargs,
                      ):
    """
    previous (layer1) and subsequent layer names (layer2) are the columns names in df

    args_list e.g. "list_years + list_labels_and_priors + Lobes"
    give it complete list of args_list including new layer list -see age example below
    give it the args_df from previous layers - new one calculated in function
    already_melted is one of "layer1" or "layer2" or "both".

    i.e. the output returns second_merge_sorted which can be used in sankey_plot.
    second_merge_sorted has the data for all the layers, and the last two layers are determined by
        inputs layer1 and layer2
    """
    # check theunmelted df
    # df[layer2+['layer1']]
    if already_melted == 'layer1':
        df_melted_layer1_layer2 = pd.melt(
            df, value_vars=layer2, id_vars=layer1).dropna()
    elif already_melted == 'layer2':
        df_melted_layer1_layer2 = pd.melt(
            df, value_vars=layer1, id_vars=layer2).dropna()
    elif already_melted == 'both':
        df_melted_layer1_layer2 = df[[layer1, layer2, 'Localising']].copy()
    elif already_melted == 'neither':
        df_melted_layer1_layer2 = pd.melt(
            df, value_vars=layer1, id_vars='Localising').dropna()
        df_melted_layer1_layer2 = pd.melt(
            df, value_vars=layer2, id_vars='Localising').dropna()

    df_melted_layer1_layer2.columns = ['layer2', 'layer1', 'Localising']
    df_layer1_layer2 = df_melted_layer1_layer2.groupby(by=['layer1', 'layer2'])[
        'Localising'].sum().reset_index()

    # checks
    # df_layer1_layer2['layer2'].unique()
    # df_layer1_layer2.shape
    # df_layer1_layer2['Localising'].sum()

    list_year_label_layer1_layer2 = args_list
    df_Nodes_Labels = pd.DataFrame(
        list_year_label_layer1_layer2, columns=['Nodes, Labels'])
    df_Nodes_Labels['indexcol'] = df_Nodes_Labels.index

    if "reverse" not in kwargs:
        if already_melted == 'both':
            df_layer1_layer2.rename(columns={'layer2': 'Source'}, inplace=True)
            df_layer1_layer2.rename(columns={'layer1': 'Target'}, inplace=True)
        else:  # defo works for layer2
            df_layer1_layer2.rename(columns={'layer1': 'Source'}, inplace=True)
            df_layer1_layer2.rename(columns={'layer2': 'Target'}, inplace=True)
    elif "reverse" in kwargs:
        df_layer1_layer2.rename(columns={'layer2': 'Source'}, inplace=True)
        df_layer1_layer2.rename(columns={'layer1': 'Target'}, inplace=True)

    if not args_df:
        good_name = pd.concat(
            [df_Year_GT, df_GT_Priors, df_Priors_Lobes], axis=0)
    elif args_df:
        good_name = pd.concat([*args_df], axis=0)
    # print('type args_df {}'.format(type(args_df)))
    # print('type good_name {}'.format(type(good_name)))
    # print('type df_layer1_layer2 {}'.format(type(df_layer1_layer2)))
    lets_give_it_a_good_name = pd.concat([good_name, df_layer1_layer2], axis=0)

    first_merge = lets_give_it_a_good_name.merge(df_Nodes_Labels,
                                                 left_on='Source', right_on='Nodes, Labels')
    first_merge.drop(columns=['Source'], inplace=True)
    first_merge.rename(columns={'indexcol': 'Source'}, inplace=True)

    second_merge = first_merge.merge(df_Nodes_Labels,
                                     left_on='Target', right_on='Nodes, Labels')
    second_merge.drop(
        columns=['Target', 'Nodes, Labels_x', 'Nodes, Labels_y'], inplace=True)
    second_merge.rename(columns={'indexcol': 'Target'}, inplace=True)

    second_merge_sorted = second_merge.sort_values(by=['Source', 'Target'])

    return second_merge_sorted, df_layer1_layer2, df_Nodes_Labels


def rename_labels(df_Nodes_Labels_Lobes_age):
    # rename TL splits:
    df_Nodes_Labels_Lobes_age.loc[df_Nodes_Labels_Lobes_age['Nodes, Labels']
                                  == 'Mesial Temporal', 'Nodes, Labels'] = 'Mesial TL'
    df_Nodes_Labels_Lobes_age.loc[df_Nodes_Labels_Lobes_age['Nodes, Labels']
                                  == 'Posterior Temporal', 'Nodes, Labels'] = 'Posterior TL'
    df_Nodes_Labels_Lobes_age.loc[df_Nodes_Labels_Lobes_age['Nodes, Labels']
                                  == 'Lateral Temporal', 'Nodes, Labels'] = 'Lateral TL'
    df_Nodes_Labels_Lobes_age.loc[df_Nodes_Labels_Lobes_age['Nodes, Labels']
                                  == 'Anterior (temporal pole)', 'Nodes, Labels'] = 'Anterior TL'
    df_Nodes_Labels_Lobes_age.loc[df_Nodes_Labels_Lobes_age['Nodes, Labels']
                                  == 'Paediatric (<7yrs)', 'Nodes, Labels'] = '<7yrs'
    df_Nodes_Labels_Lobes_age.loc[df_Nodes_Labels_Lobes_age['Nodes, Labels']
                                  == 'Adult (>7yrs)', 'Nodes, Labels'] = '>7yrs'

    df_Nodes_Labels_Lobes_age.loc[df_Nodes_Labels_Lobes_age['Nodes, Labels']
                                  == 'Basal (including Fusiform OTMG)', 'Nodes, Labels'] = 'Basal TL'
    df_Nodes_Labels_Lobes_age.loc[df_Nodes_Labels_Lobes_age['Nodes, Labels']
                                  == 'Complex Behavioural', 'Nodes, Labels'] = 'Complex Behaviour'
    df_Nodes_Labels_Lobes_age.loc[df_Nodes_Labels_Lobes_age['Nodes, Labels']
                                  == 'Spontaneous Semiology (SS)', 'Nodes, Labels'] = 'SS'
    df_Nodes_Labels_Lobes_age.loc[df_Nodes_Labels_Lobes_age['Nodes, Labels']
                                  == 'Epilepsy Topology (ET)', 'Nodes, Labels'] = 'ET'
    df_Nodes_Labels_Lobes_age.loc[df_Nodes_Labels_Lobes_age['Nodes, Labels']
                                  == 'Cortical Stimulation (CS)', 'Nodes, Labels'] = 'CS'
    df_Nodes_Labels_Lobes_age.loc[df_Nodes_Labels_Lobes_age['Nodes, Labels']
                                  == 'Seizure-Freedom Only', 'Nodes, Labels'] = 'SF only'
    df_Nodes_Labels_Lobes_age.loc[df_Nodes_Labels_Lobes_age['Nodes, Labels']
                                  == 'SF and Concordance', 'Nodes, Labels'] = 'SF & Concordance'
    df_Nodes_Labels_Lobes_age.loc[df_Nodes_Labels_Lobes_age['Nodes, Labels']
                                  == 'Concordance and sEEG', 'Nodes, Labels'] = 'sEEG & Concordance'
    df_Nodes_Labels_Lobes_age.loc[df_Nodes_Labels_Lobes_age['Nodes, Labels']
                                  == 'Spasms - epileptic/infantile', 'Nodes, Labels'] = 'Spasms'
    df_Nodes_Labels_Lobes_age.loc[df_Nodes_Labels_Lobes_age['Nodes, Labels']
                                  == 'Postictal Descriptions', 'Nodes, Labels'] = 'Postictals'
    df_Nodes_Labels_Lobes_age.loc[df_Nodes_Labels_Lobes_age['Nodes, Labels']
                                  == 'Autonomous-Vegetative', 'Nodes, Labels'] = 'Autonomic'
    df_Nodes_Labels_Lobes_age.loc[df_Nodes_Labels_Lobes_age['Nodes, Labels']
                                  == 'CING', 'Nodes, Labels'] = 'Cingulate'
    df_Nodes_Labels_Lobes_age.loc[df_Nodes_Labels_Lobes_age['Nodes, Labels']
                                  == 'INSULA', 'Nodes, Labels'] = 'Insula'
    df_Nodes_Labels_Lobes_age.loc[df_Nodes_Labels_Lobes_age['Nodes, Labels']
                                  == 'OTHER', 'Nodes, Labels'] = 'Other'
    df_Nodes_Labels_Lobes_age.loc[df_Nodes_Labels_Lobes_age['Nodes, Labels']
                                  == 'Mesial TL', 'Nodes, Labels'] = 'mTL'
    df_Nodes_Labels_Lobes_age.loc[df_Nodes_Labels_Lobes_age['Nodes, Labels']
                                  == 'Posterior TL', 'Nodes, Labels'] = 'pTL'
    df_Nodes_Labels_Lobes_age.loc[df_Nodes_Labels_Lobes_age['Nodes, Labels']
                                  == 'Anterior TL', 'Nodes, Labels'] = 'aTL'
    df_Nodes_Labels_Lobes_age.loc[df_Nodes_Labels_Lobes_age['Nodes, Labels']
                                  == 'Postictal Descriptions', 'Nodes, Labels'] = 'Postictals'

    df_Nodes_Labels_Lobes_age.loc[df_Nodes_Labels_Lobes_age['Nodes, Labels']
                                  == 'Ictal Speech', 'Nodes, Labels'] = 'Ictal Speech: Formed Words'
    df_Nodes_Labels_Lobes_age.loc[df_Nodes_Labels_Lobes_age['Nodes, Labels'] ==
                                  'Vocalisation', 'Nodes, Labels'] = 'Vocalisation: Unintelligible Noises'

    return df_Nodes_Labels_Lobes_age


def sankey_plot(
    label,
    color,
    source,
    target,
    value,
    link_colour=None,
    title="Semio2Brain Database Sankey Diagram:\nLocalising Datapoints Flow",
    height=772,
    width=950,
    pad=10,
    thickness=30,
    fontsize=10,
    updatemenus=False,
    alpha=0.4,
):
    """
    e.g.
    label=df_Nodes_Labels['Nodes, Labels'].dropna(),
    color=df_Nodes_Labels['Color'],
    source=second_merge_sorted['Source'],
    target=second_merge_sorted['Target'],
    value=second_merge_sorted['Localising']
    """
    data_trace = dict(
        type='sankey',
        domain=dict(
            x=[0, 1],
            y=[0, 1]
        ),
        orientation="h",
        valueformat=".0f",
        node=dict(
            pad=pad,
            thickness=thickness,
            line=dict(
                color="black",
                width=0.5
            ),
            label=label,
            color=color,
        ),
        link=dict(
            source=source,
            target=target,
            value=value,
            color=link_colour,
        )
    )
    if not updatemenus:
        layout = dict(
            title=title,
            height=height,
            width=width,
            font=dict(
                size=fontsize
            ),
        )
    if updatemenus:
        layout = dict(
            title=title,
            height=height,
            width=width,
            font=dict(
                size=fontsize
            ),
            updatemenus=[
                dict(
                    y=0.8,
                    buttons=[
                        dict(
                            label='Light',
                            method='relayout',
                            args=['paper_bgcolor', 'white']
                        ),
                        dict(
                            label='Dark',
                            method='relayout',
                            args=['paper_bgcolor', 'black']
                        ),
                        dict(
                            label='Teal',
                            method='relayout',
                            args=['paper_bgcolor', 'teal']
                        ),
                        dict(
                            label='Lightblue',
                            method='relayout',
                            args=['paper_bgcolor', 'lightblue']
                        )
                    ]
                ),
                dict(
                    y=0.7,
                    buttons=[
                        dict(
                            label='Thick',
                            method='restyle',
                            args=['node.thickness', 15]
                        ),
                        dict(
                            label='Thin',
                            method='restyle',
                            args=['node.thickness', 8]
                        )
                    ]
                ),
                dict(
                    y=0.6,
                    buttons=[
                        dict(
                            label='Tiny gap 6',
                            method='restyle',
                            args=['node.pad', 6]
                        ),
                        dict(
                            label='Small gap 8',
                            method='restyle',
                            args=['node.pad', 8]
                        ),
                        dict(
                            label='Medium gap 10',
                            method='restyle',
                            args=['node.pad', 10]
                        ),
                        dict(
                            label='Med-Large gap 12',
                            method='restyle',
                            args=['node.pad', 12]
                        ),
                        dict(
                            label='Large gap 15',
                            method='restyle',
                            args=['node.pad', 15]
                        ),
                        dict(
                            label='Very Large gap 20',
                            method='restyle',
                            args=['node.pad', 20]
                        )
                    ]
                ),
                dict(
                    y=0.5,
                    buttons=[
                        dict(
                            label='Snap',
                            method='restyle',
                            args=['arrangement', 'snap']
                        ),
                        dict(
                            label='Perpendicular',
                            method='restyle',
                            args=['arrangement', 'perpendicular']
                        ),
                        dict(
                            label='Freeform',
                            method='restyle',
                            args=['arrangement', 'freeform']
                        ),
                        dict(
                            label='Fixed',
                            method='restyle',
                            args=['arrangement', 'fixed']
                        )
                    ]
                ),
                dict(
                    y=0.4,
                    buttons=[
                        dict(
                            label='Horizontal',
                            method='restyle',
                            args=['orientation', 'h']
                        ),
                        dict(
                            label='Vertical',
                            method='restyle',
                            args=['orientation', 'v']
                        )
                    ]

                )
            ],
        )

    fig = dict(data=[data_trace], layout=layout)
    iplot(fig, validate=False)

    # https://community.plotly.com/t/sankey-graphs-blank-when-saved-as-svg/20312
    # fig = go.Figure(data=[data], layout=layout)
    # pio.write_image(fig, "./output/graphs/")
    return fig
