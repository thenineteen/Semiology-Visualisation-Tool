# This is a powershell script to convert
# .doc word files to .docx en batch
# downloaded from https://github.com/Apoc70/Convert-WordDocument
# license: MIT License, Copyright (c) 2017 Thomas Stensitzki

## allow access to folders and scripts for this session:
set-executionpolicy remotesigned
# powershell.exe -ExecutionPolicy Unrestricted

## This sets directory to this file:
# Set-Location -Path  C:\Users\ali_m\AnacondaProjects\PhD\Epilepsy_Surgery_Project\preprocessing

# change directory to folder where Convert-WordDocument was downloaded to
Set-Location (Get-ChildItem C:\** -Filter *Convert-WordDocument -Recurse | % { $_.FullName }) 

# figure a way to supress the errors "PersmissionDenied/Unauthorized access" etc
# tried try{}/catch{} doesn't work

# Now convert all the .doc to .docx (first one is as a test):
# .\Convert-WordDocument.ps1 -SourcePath L:\script_test_word_docs -IncludeFilter *.doc
.\Convert-WordDocument.ps1 -SourcePath L:\word_docs\1Script_Word_docs_2001_to_2011_to_docx -IncludeFilter *.doc
