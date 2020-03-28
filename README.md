# mega_analysis

## Epilepsy Semiology Visualisation Tool:
Thousands of patient level semiology data from journal publications with localisation and lateralisation numbers collected based on the following groun-truths:

* post-operative seizure freedom, 
* imaging & EEG concordance, (could include PET, SPECT, MEG but this can be filtered) 
* sEEG/stimulation studies

The data also are tagged to reduce publications bias and enhance visualisation of invasive EEG electrode targets by removing specific paper/patient level priors: 

* Epilepsy Topology (ET): when a study looks at patients with epilepsy with e.g. temporal lobe onset
* Spontaneous Semiology (SS): when a study looks either at all patients with a particular semiology e.g. epigastric rising or between selected dates
* sEEG/cortical stimulation studies


## Brief workings:
In brief, this software cleans the DataFrame of data, pivots occurences of semiology, allowing for semiology_dictionary ontology replacement regex searches, maps the documented localisations to gif parcellations and can scale these mappings using different scalers/transformers. 
Data can be filtered based on the above ground truth and journal priors. 


## Branches
* Master branch - to be used with slicer module for 3D visualisation
  ** (merged from separate repo (https://github.com/fepegar/EpilepsySemiology))
* MegaAnalysis-March2020 branch - original verbose module for development and progress stats 
  ** (thenineteen jupyter backwards compatibility)

