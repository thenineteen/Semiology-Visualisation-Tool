***Ali Alim-Marvasti Dec 2018***
**Wellcome/EPSRC Centre for Interventional and Surgical Sciences WEISS**
***University College London***

First thing is first: 
1. the sample PDFs with 'PDF_form_example' are the only PDFs which are read by the PyPDF2 methods of .getFields() and .getFormTextFields()
2. Currently .getFormTextFields() is used on line 31 - but .getFields() works best with these PDFs 'PDF_form_example'
3. What we want is for the other PDFs to be read which isn't working currently. I've also tried pdfminer.six - can't even read number of pages
   1. not an excryption problem as read_pdf.isEncrypted returns False
what is the solution?

*MetaData*

*Files*

*Installation*




*Running from command line cmd*
*Syntax and Exceptions*