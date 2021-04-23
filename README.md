<p align="center">
  <img src="images/SVT%20branding%20purple%20medium%202.png">
</p>
<p align="center"> v 1.8.1 </p> 

<h1 align="center"> Seizure Semiology-to-Brain Visualisation Tool (SVT) </h1>


  
<h2 align="center"> Seizure Semiology lateralisation and localisation information from 4,643 patients' data from 309 included original journal papers
<h3 align="center"> 11230 localising and 2391 lateralising datapoints

<p align="center"> For research purposes only. Not for clinical use (yet). </p> 


[![Build status](https://img.shields.io/travis/thenineteen/Semiology-Visualisation-Tool/master.svg?label=Travis%20CI%20build&logo=travis)](https://travis-ci.org/thenineteen/Semiology-Visualisation-Tool)  [![Coverage Status](https://coveralls.io/repos/github/thenineteen/Semiology-Visualisation-Tool/badge.svg?branch=master)](https://coveralls.io/github/thenineteen/Semiology-Visualisation-Tool?branch=master)

![3D Slicer module screenshot](images/all_automatisms.png)
Above Figure from beta-version:
849 Patients with automatisms have an epileptogenic zone localising mostly to the mesial temporal lobe.
124 of these lateralise, mainly ipsilaterally.


Below: Sankey Diagram overview of Semio2Brain Database, Filters, SemioDict, and broad localisation mapppings. SVT uses finer GIF localisation parcellations. 
![Sankey Marvasti Modarres Diagram](images/Sankey/Beautified%206%20layer%20colour%20coded%20lumped%20semiology%20and%20TL%20subregions.png)




## Installation Guide
1. Clone (or [download](https://github.com/thenineteen/Semiology-Visualisation-Tool/archive/master.zip) and extract) this repository
2. Download a [**Preview Release** of 3D Slicer](https://download.slicer.org/) (not the Stable version)
3. Install and open Slicer
4. Go to the menu `Edit` > `Application Settings` > `Modules` > `Additional module paths` > `Add` (you may have to click on the double arrows to the right of Additional Module Paths)
5. Click on the directory to which you cloned this repository > click on the `slicer` folder and click `Select Folder`
6. Click on `OK` and restart Slicer when prompted
7. To open the module, click on the magnifier and search for `Semiology`, then click on the module as below.
It may take a few minutes to load for the first time.
![Top image: step 7.](https://github.com/thenineteen/Semiology-Visualisation-Tool/blob/master/images/instructions.jpg)

8. You might need to restart Slicer again, if prompted
9. You can now click on the "Load data" button as below, and the SVT software will soon be ready for you to query the database:
![Bottom image: location of "Load data" button for step 9.](https://github.com/thenineteen/Semiology-Visualisation-Tool/blob/master/images/instructions2.jpg)

### Funding
Wellcome/EPSRC Centre for Interventional and Surgical Sciences (WEISS) (203145Z/16/Z).
