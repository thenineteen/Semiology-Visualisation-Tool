***Ali Alim-Marvasti Dec 2018***
**Wellcome/EPSRC Centre for Interventional and Surgical Sciences WEISS**
***University College London***

Developed and tested on MSI GS65 8RF Stealth Thin 32GB GTX 1070 Max-Q
running: Windows 10  Python 3.6.6 , Anaconda 1.9.6, Windows PowerShell 

 
*MetaData*

*Files*

*Installation*
1. If you have new raw clinical .doc files, you will need to download this powershell script to convert them to .docx en batch:
download from https://github.com/Apoc70/Convert-WordDocument
license: MIT License, Copyright (c) 2017 Thomas Stensitzki
this is incorporated in this Epilepsy_Suergery_Project under doc_to_docx.ps1 script; however not available from PyPI so will need to be downloaded

2. word_preprocess
After converting .doc to .docx, word documents are preprocessed for text mining. 

3. pdf_preprocess
Epilepsy PDFs were produced using Adobe LiveCycle, dynamic XML format. 
Regular open source software and scripts are unable to read these (tested pdfminer.six, PyPDF2, and others)

*Running from command line cmd*

*Syntax and Exceptions*