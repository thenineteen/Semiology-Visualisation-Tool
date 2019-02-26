***Ali Alim-Marvasti Dec 2018***
**Wellcome/EPSRC Centre for Interventional and Surgical Sciences WEISS**
***University College London***

Developed and tested on MSI GS65 8RF Stealth Thin 32GB GTX 1070 Max-Q
running: Windows 10  Python 3.6.6 , Anaconda 1.9.6, Windows PowerShell 

 
*MetaData*

*Scripts/Files*
1. doc_to_docx.ps1:
   If you have new (e.g. neurophys docs) raw clinical .doc files, you will need to download this powershell script to convert them to .docx en batch by hand (prior to installation):
download from https://github.com/Apoc70/Convert-WordDocument
license: MIT License, Copyright (c) 2017 Thomas Stensitzki
Direct download reason: not python script and thus not available from PyPI.

Next, copy and paste the code in doc_to_docx.ps1 script onto powershell window (opened as administrator) -
remember to update the directory paths in the script as required, before running.

(Probably best for large numbers of documents to iterate each folder in turn rather than using the recursive option, as MS word can crash often and uses alot of the available RAM (upto 90% of my 32GB).

Completed 18th Jan 2019

2. word_preprocess.py:
After converting .doc to .docx, word documents are preprocessed for text mining.
.rtf is also preprocessed.
Ensure you have created a new folder as specified in word_preprocess to avoid save errors.
[] combine texts belonging to same person (append) from file name or name within .docx
[/] pop names and psuedononymise - Feb 2019
[] make them searchable (?regex)


3. pdf_preprocess.py:
Epilepsy PDFs were produced using Adobe LiveCycle, dynamic XML format. 
Regular open source software and scripts are unable to read these (tested pdfminer.six, PyPDF2, and others)

*Installation*


*Running from command line cmd*

*Syntax and Exceptions*
# 0. convert .doc to docx and .rtf to .txt and .pdf to pdf readable/docx/txt
# 1. run main_docx_preprocess()
writes .txt files to three folders which need checking as below.
creates a json dictionary with sensitive personalised data and keys.
This json dictinary is updated ni step 3.
# 2. check results (output, 3 folders, json)
folder1: docx to txt output
folder2: docx_xml function to txt output
folder3: txt with redacted name,DOB,MRN output
json dictionary: with all sensitive data keys 
# 3. add outcomes using find_MRN_label_outcomes()
After main_docx_preprocess, run the gold_outcomes_MRNs() function in outcomes.py to get list of labels
and add the labels to the above keys using the find_MRN_label_outcomes() function in json_keys_read.py.
Creates new json dictionary and adds the keys to the above keys created when running the main function. 
# 4. outcomes_count()
Now count the number of Gold ILAE 1, non-gold standard resections and #s of patients who didn't
have surgery in the keys produced above. Doesn't change any files, prints results. 

##From Jupyter Notebook, can run after importing like this:
import sys

sys.path.insert(0, r"C:\Users\ali_m\AnacondaProjects\PhD\Epilepsy_Surgery_Project\preprocessing")

from json_keys_read import find_MRN_label_outcomes, outcomes_count
from main_docx_preprocess import main_docx_preprocess
from word_preprocess import args_for_loop, update_txt_docx, save_as_txt
from word_preprocess import epilepsy_docx_to_txt, epilepsy_docx_xml_to_txt 
from word_preprocess import anonymise_name_txt, anonymise_DOB_txt, anon_hosp_no
from Epilepsy_Surgery_Project.crosstab import outcomes