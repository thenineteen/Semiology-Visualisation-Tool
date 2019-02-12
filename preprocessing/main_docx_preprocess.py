from preprocessing.word_preprocess import epilepsy_docx, epilepsy_docx_xml
from preprocessing.word_preprocess import anonymise_name_txt, save_as_txt
from preprocessing.word_preprocess import anonymise_DOB_txt
import os


def main_docx_preprocess(path_to_folder, *paragraphs, read_tables=False,
                         clean=False, save_path="L:\\word_docs\\test_texxts_name\\"):
    """
    This runs the functions from word_preprocess.py

    run like this:
    path_to_folder = 'L:\\word_docs\\test_anonymise\\'
    
    main_docx_preprocess(path_to_folder, read_tables=True, clean=False)
    
    Runs docx first. if this fails, runs epilepsy_docx_xml.
    If both fail, gives error message. 
    """
    n_docx = 0
    n_xml = 0
    n_docx_name_anon = 0
    n_xml_name_anon = 0
    n_DOB_anon = 0
    n_xml_DOB_anon = 0

    for docx_file in os.listdir(path_to_folder):
        path_to_doc = os.path.join(path_to_folder, docx_file)

        pt_txt, pt_docx_list, pt_meds_list = epilepsy_docx(
            path_to_doc, *paragraphs, read_tables=False, clean=False)

        n_docx += 1

        # anonymise names first
        try:  # sometimes there is no actual name after "Name:" in the file
            pt_txt = anonymise_name_txt(pt_txt, path_to_doc)
            n_docx_name_anon += 1

        except AttributeError:
             # if no name found, run the other docx XML function
            try:
                pt_txt = epilepsy_docx_xml(path_to_doc)
                n_xml += 1
                pt_txt = anonymise_name_txt(pt_txt, path_to_doc, xml=True)
                n_xml_name_anon += 1
            except:
                print("anonymise_name (xml=True) failed for {}".format(path_to_doc))
                continue

        except:
            print("anonymise_name_txt failed for {}".format(path_to_doc))
            continue

        finally:  # whether it did anonymise name or not, save the txt
            save_as_txt(path_to_doc, pt_txt, save_path)

    return print('number of docx files read using epilepsy_docx() = \
             \t{} \nof which number anonymise_name_txt(), DOB =\
             \t{}, {}.\nnumber needing epilepsy_docx_xml()\
             \t= \t\t{} \nof which number anonymise_name_txt(), DOB =\
                 \t{}, {}.'
                 .format(n_docx, n_docx_name_anon, n_DOB_anon, n_xml,
                         n_xml_name_anon, n_xml_DOB_anon))
