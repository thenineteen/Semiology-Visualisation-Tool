from mega_analysis.Bayesian.Bayesian_marginals import p_GIFs, p_Semiology_and_Localisation

p_S_norm, p_Loc_norm, p_S_notnorm, p_Loc_notnorm = p_Semiology_and_Localisation(publication_prior='full', test=False)
p_GIF_norm, p_GIF_notnorm = p_GIFs(global_lateralisation=False,
                                       include_paeds_and_adults=True,
                                       include_only_postictals=False,
                                       symptom_laterality='neutral',
                                       dominance='neutral',
                                       )
