Output of MEGA_ANALYSIS is Venn diagrams, text output and preprocessed DataFrame: df
Output of QUERY_SEMIOLGY/QUERY_INTERSECTION_TERMS is a table of relevant query results: inspect_result
Output of melt_then_pivot_query is a single row of relevant results: pivot_result
Output of pivot_result_to_pixel_intensities is a single row, with pixel intensities as values: pivot_result_intensities
Output of mapping.pivot_result_to_one_map is a table of Gif parcellations and their relevant pixel intensities: all_gifs
 many things will and can affect the output/visualisation so needs calibration.

Memo: relevant factors include:

curve fitting: scale_factor, number of quantiles, and exact curve-fitting method (linear, normal/skew, chi2-dist) 

mappings: localisations-to-gif-parcellation mappings

data collection: ​​the hierarchical "postcode" anatomy methodology affects the heatmap