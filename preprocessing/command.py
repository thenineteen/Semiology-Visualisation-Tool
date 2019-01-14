"""
Command-line entry point from setup links to this file.
It should be called with "Process_Epilepsy_PDFs" followed by inputfolderpath
details and outputpath details

"""

from argparse import ArgumentParser
from preprocessing.main_preprocessing import main_preprocessing
# from preprocessing.pdf_preprocess import
import yaml


def process_pdfs():
    parser = ArgumentParser(description="Epilepsy PDF data processing")
    parser.add_argument('pdf_folder_path')  # where the PDFs are
    parser.add_argument('keys_of_pdf_to_remove')  # add default later
    parser.add_argument('--true', '-t', action='store_true')
    # -t: future use to be able to run or omit a section of the code
    arguments = parser.parse_args()

    output1 = main_preprocessing(pdf_folder_path=arguments.pdf_folder_path,
                                 k=arguments.keys_of_pdf_to_remove)
    # output2 = output1.SOMEFUNCTION(arguments.true)

    try:
        if arguments.true:
            pass
        else:
            pass
    except(TypeError):
            pass

if __name__ == "__main__":  # why is this here?
    process_pdfs()
