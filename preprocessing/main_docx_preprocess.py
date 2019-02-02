from preprocessing.word_preprocess import *
import os


def main_docx_preprocess(path_to_folder, *paragraphs, read_tables=False,
                         clean=False):
    for docx_file in path_to_folder:  # cycle through all pt files
        path_to_doc = os.path.join(path_to_folder, docx_file)
        pt_txt, pt_docx_list, pt_meds_list = epilepsy_docx(
            path_to_doc, *paragraphs, read_tables=False, clean=False)

        try:  # sometimes there is no actual name after "Name:" in the file
            pt_txt = anonymise_txt(pt_txt)
        except AttributeError:
            # if no name found, run the other docx text read function
            pt_txt_xml = epilepsy_docx_xml(path_to_doc)
            pt_txt_xml = anonymise_txt(pt_txt_xml, xml=True)
