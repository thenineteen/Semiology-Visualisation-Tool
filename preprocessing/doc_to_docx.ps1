# This is a powershell script to convert
# .doc word files to .docx en batch
# downloaded from https://github.com/Apoc70/Convert-WordDocument
# license: MIT License, Copyright (c) 2017 Thomas Stensitzki

# allow access to folders and scripts for this session
powershell.exe -ExecutionPolicy Unrestricted

# change directory to folder where Convert-WordDocument was downloaded to
Set-Location (Get-ChildItem C:\** -Filter *Convert-WordDocument -Recurse | % { $_.FullName })

# figure a way to supress the errors "PersmissionDenied/Unauthorized access" etc
# tried try{}/catch{} doesn't work

# Now convert all the .doc to .docx
.\Convert-WordDocument.ps1 -SourcePath L:\copy_word_docs -IncludeFilter *.doc