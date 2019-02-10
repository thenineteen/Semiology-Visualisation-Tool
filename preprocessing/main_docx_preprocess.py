from preprocessing.word_preprocess import epilepsy_docx, epilepsy_docx_xml
from preprocessing.word_preprocess import anonymise_name_txt, save_as_txt
import os


def main_docx_preprocess(path_to_folder, *paragraphs, read_tables=False,
                         clean=False):
    """
    This runs the functions from word_preprocess.py

    run like this:
    path_to_folder = 'L:\\word_docs\\test_anonymise\\'
    n_docx, n_docx_name_anon, n_xml, n_xml_name_anon =
        main_docx_preprocess(path_to_folder, read_tables=True, clean=False)
    """
    n_docx = 0
    n_xml = 0
    n_docx_anon = 0
    n_xml_anon = 0

    for docx_file in os.listdir(path_to_folder):
        path_to_doc = os.path.join(path_to_folder, docx_file)

        pt_txt, pt_docx_list, pt_meds_list = epilepsy_docx(
            path_to_doc, *paragraphs, read_tables=False, clean=False)

        n_docx += 1

        try:  # sometimes there is no actual name after "Name:" in the file
            pt_txt = anonymise_name_txt(pt_txt)
            n_docx_name_anon += 1
        except AttributeError:
            # if no name found, run the other docx text read function
            pt_txt_xml = epilepsy_docx_xml(path_to_doc)
            n_xml += 1
            pt_txt_xml = anonymise_name_txt(pt_txt_xml, xml=True)
            n_xml_name_anon += 1

    return print(n_docx, n_docx_name_anon, n_xml, n_xml_name_anon)
