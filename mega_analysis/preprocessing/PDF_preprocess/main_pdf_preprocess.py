"""
This uses the PDF_preprocess to anonymise all the PDFs and write json file
"""

from pathlib import Path
import json
from preprocessing.pdf_preprocess import PyPDF2_getFormTextFields
from preprocessing.pdf_preprocess import anonymise, writeData

# USER CHANGES THIS with input

pdfs_are_here = (
    'C:\\Users\\ali_m\\AnacondaProjects\\PhD\\'
    'Epilepsy_Surgery_Project\\preprocessing\\tests\\test pdfs'
)
# test pdfs pathname
# e.g. 'Gender List Box' on the samples that work
keys_of_pdf_to_remove = 'Name'


def main_pdf_preprocess(pdf_folder_path=pdfs_are_here, k=keys_of_pdf_to_remove):
    """
    Opens all PDF files in directory, removes labels, writes json file.
    Returns number of PDF files.
    Main Preprocessing calls 3 function in pdf_preprocess.
    First function it calls works best with the the sample PDFs
    PDF_form_example when the method it calls is changed to
    read_pdf.getFields() (see comment on line 32)
    """
    superdict = {}
    dir_path = Path(pdfs_are_here)
    pdf_files = list(dir_path.glob('*.pdf'))  # convert result to a list
    for pdffile in pdf_files:
        print(pdffile)
        fields = PyPDF2_getFormTextFields(pdffile)
        (tuplist, label) = anonymise(fields, keys_of_pdf_to_remove)
        writeData(superdict, tuplist, label)

    with open(
        'D:\\Ali USB Backup\\1 PhD\\AnacondaProjects\\PhD\\All_Data.json', 'w'
            ) as file:
        file.write(json.dumps(superdict))
    return len(pdf_files)
