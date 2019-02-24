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
[] pop names and psuedononymise
[] make them searchable (?regex)


3. pdf_preprocess.py:
Epilepsy PDFs were produced using Adobe LiveCycle, dynamic XML format. 
Regular open source software and scripts are unable to read these (tested pdfminer.six, PyPDF2, and others)

*Installation*


*Running from command line cmd*

*Syntax and Exceptions*

# 1. run main_docx_preprocess()
# 2. check results (output, 3 folders, json)
folder1: docx to txt output
folder2: docx_xml function to txt output
folder3: txt with redacted name,DOB,MRN output
json dictionary: with all sensitive data keys 
# 3. add outcomes using find_MRN_label_outcomes()
creates new json dictionary and adds the keys to the above
I think you must have already made the json file for it to work