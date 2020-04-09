# mega_analysis

[![Build status](https://img.shields.io/travis/thenineteen/Semiology-Visualisation-Tool/master.svg?label=Travis%20CI%20build&logo=travis)](https://travis-ci.org/thenineteen/Semiology-Visualisation-Tool)

## Epilepsy Semiology Visualisation Tool:

![](resources/SVT_All_Automatisms.jpg)
Figure:
849 Patients with automatisms have an epileptogenic-zone localising mostly to the mesial temporal lobe.
124 of these lateralise, mainly ipsilaterally.


Thousands of patient level semiology data from journal publications with localisation and lateralisation numbers collected based on the following ground-truths:

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


## Installation Guide
1. Clone (or [download](https://github.com/thenineteen/Semiology-Visualisation-Tool/archive/master.zip) and extract) this repository
2. Download a [**Preview Release** of 3D Slicer](https://download.slicer.org/) (not the Stable version)
3. Install and open Slicer
4. Go to the menu `Edit` > `Application Settings` > `Modules` > `Additional module paths` > `Add` (you may have to click on the double arrows to the right of Additional Module Paths)
5. Click on the directory to which you cloned this repository > click on the `slicer` folder and click `Select Folder`
6. Click on `OK` and restart Slicer when prompted
7. To open the module, click on the magnifier and search for `Semiology`
8. You might need to restart Slicer again, if prompted
