<p align="center">
  <img src="images/SVT%20branding%20purple%20medium%202.png">
</p>
<p align="center"> v 1.8.1 </p> 

<h1 align="center"> Seizure Semiology-to-Brain Visualisation Tool (SVT) </h1>


  
<h2 align="center"> Seizure Semiology lateralisation and localisation values
  <br> 11230 localising and 2391 lateralising datapoints
  <br> 4,643 patients' data from 309 included original journal articles
  </h2>
</h2>  

<br>  
<p align="center"> For research purposes only. Not for clinical use (yet).


[![Build status](https://img.shields.io/travis/thenineteen/Semiology-Visualisation-Tool/master.svg?label=Travis%20CI%20build&logo=travis)](https://travis-ci.org/thenineteen/Semiology-Visualisation-Tool)  [![Coverage Status](https://coveralls.io/repos/github/thenineteen/Semiology-Visualisation-Tool/badge.svg?branch=master)](https://coveralls.io/github/thenineteen/Semiology-Visualisation-Tool?branch=master)



SVT has low and high-resolution visualisations, uses Bayesian inference to mitigate publication bias from **Topological Studies (TS)** and can combine semiologies and data-subset queries using inverse variance weighted means by modelling brain parcellations as binomial random variables for each semiology. For more information on topological studies see our wiki page. 

# Citing
If you use the underlying database (Semio2Brain) or the software (SVT), please cite the original paper describing the database and localisation results:
**Ali Alim-Marvasti, Gloria Romagnoli, Karan Dahele, Hadi Modarres, Fernando Pérez-García, Rachel Sparks, Sebastien Ourselin, Matthew J Clarkson, Fahmida Chowdhury, Beate Diehl, John S Duncan. Probabilistic Landscape of Seizure Semiology Localising Values. Brain Communications. 2022 (In Press)**

<img src="https://github.com/thenineteen/Semiology-Visualisation-Tool/blob/master/images/GOSH%20April%202021.png">




<img src="https://github.com/thenineteen/Semiology-Visualisation-Tool/blob/master/images/GOSH%20April%202021%202.png">
<br>



<img src="https://github.com/thenineteen/Semiology-Visualisation-Tool/blob/master/images/GOSH%20April%202021%203.png">





[See our Wiki page for more software details, including on semiological categories and their semantic synonyms.](https://github.com/thenineteen/Semiology-Visualisation-Tool/wiki)



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
