"""
Extract all the labels from all the pdf’s.
Then remove desired labels from files:
(e.g. whether they needed icEEG, not for surgery, location of EZ).
Store labels and raw pdf’s separately both with the same keys.

Acknowledgement: Sadegh Shahrbaf
"""

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
import PyPDF2
import json
import uuid
# from pathlib import *
import copy
import os


def PyPDF2_getFormTextFields(filepath):
    """ 1.1 This function opens the pdf and extracts all fields and
    returns pdf_form_data as a dict"""

    with open(filepath, "rb") as pdf_file:
        read_pdf = PyPDF2.PdfFileReader(pdf_file)
        if read_pdf.isEncrypted:
            print('file encrypted')
            read_pdf.decrypt('semiology')
        number_of_pages = read_pdf.getNumPages()
        print('number of pages =', number_of_pages)

        pdf_form_data = read_pdf.getFormTextFields()  # read_pdf.getFields()
        print(
             "\n\n\n.getFormTextFields()=the following dictionary\n",
             pdf_form_data)
    return pdf_form_data


def anonymise(pdf_form_data, label_key):
    """ 1.2 this function pops label (using label_key) from pdf_form_data dict
        and returns a list of tuples (keys of dict where labels have been
        removed, values=predictors/features) along with popped label:
        keyvals_removedlabel = list of tuples and
        pdf_form_data_GENDERlabel = value of popped label"""
    pdf_form_data_removedlabel = copy.deepcopy(pdf_form_data)
    pdf_form_data_GENDERlabel = pdf_form_data_removedlabel.pop(label_key, None)
    try:
        pdf_form_data_GENDERlabel = pdf_form_data_GENDERlabel['/V']
        keyvals_removedlabel = [(k, pdf_form_data_removedlabel[k]['/V'])
                                for k in pdf_form_data_removedlabel.keys()
                                if '/V' in pdf_form_data_removedlabel[k] and
                                pdf_form_data_removedlabel[k]['/V'] != '']
        return (keyvals_removedlabel, pdf_form_data_GENDERlabel)
    except:
        print("check this PDF doesn't have a '/V' key for the chosen label")


# 1.3
# now we will store the label as a file
# this saves the text files with the same name
# superdict = {}
def writeData(superdict, keyvals_removedlabel, pdf_form_data_GENDERlabel):
    """
    This writes two json files, one to "unlabelled" data folder and
    the other to "label" data folder. The filenames match
    and one file in each folder (two files) are created per pdf.
    The json file is a list of lists where the first element is the pdf key
    and the second is the value in the original pdf.
    """
    newid = str(uuid.uuid4())
    # with open('D:\\Ali USB Backup\\1 PhD\\AnacondaProjects\\PhD\\\
    # unlabelled data\\' + newid + '.json', 'w') as file:
    with open(
         os.path.join(test_files, 'unlabelled data') +
         newid + '.json', 'w') as file:

        file.write(json.dumps(keyvals_removedlabel))
    with open(os.path.join(test_files, 'label') +
              newid + '.json', 'w') as file:
        file.write(pdf_form_data_GENDERlabel)
    superdict[newid] = keyvals_removedlabel

test_files = (
     "C:\\Users\\ali_m\\AnacondaProjects\\PhD\\"
     "Epilepsy_Surgery_Project\\preprocessing\\tests"
)
