import yaml
import json
import os
import pytest
from unittest import TestCase
from ..word_preprocess import args_for_loop, update_txt_docx, save_as_txt
from ..word_preprocess import epilepsy_docx_to_txt, epilepsy_docx_xml_to_txt 
from ..word_preprocess import name_pattern_regex, pt_txt_replace
from ..word_preprocess import anonymise_name_txt, anonymise_DOB_txt, anon_hosp_no
from ..main_docx_preprocess import main_docx_preprocess

def read_fixture(filename):
    """opens the fixtures file"""
    with open(os.path.join('L:\\word_docs\\pytest\\',
                           filename)) as f:
        fixtures_json_answer = json.load(f)
        return fixtures_json_answer


# @pytest.mark.parametrize("fixture", read_fixture())  # cycle through all
# #  this decorator stores each key of the fixture_json_answer as fixture
# #  if using this, add fixture as argument to below function
def test_anonymise_single(path_to_folder = 'L:\\word_docs\\pytest\\test_anonymise_single\\'):

    main_docx_preprocess(path_to_folder, read_tables=False,
                     clean=False, save_path="L:\\word_docs\\pytest\\test_texxts\\",
                     json_dictionary_file = 'L:\\word_docs\\pytest\\test_keys.json',
                     DOCX=True)

    with open ('L:\\word_docs\\pytest\\test_keys.json') as tk:
        test_json_data = json.load(tk)
    fixture = read_fixture(filename='fixture_anonymise_single.json')

    assert test_json_data == fixture


def test_skipNeurophysVTreports_and_anonnamexmlTrue():
    path_to_folder = 'L:\\word_docs\\pytest\\test_anon_name_xml_True\\'
    main_docx_preprocess(path_to_folder, read_tables=False,
                        clean=False, save_path="L:\\word_docs\\pytest\\test_texxts\\",
                        json_dictionary_file = 'L:\\word_docs\\pytest\\test_keys.json',
                        DOCX=True)
    
    with open ('L:\\word_docs\\pytest\\test_keys.json') as tk:
        test_json_data = json.load(tk)
    fixture = read_fixture(filename='fixture_name_anon_xml_True.json')

    assert test_json_data == fixture


def test_failures():  # blank and ward template docx
    with pytest.raises(AttributeError):
        path_to_folder = 'L:\\word_docs\\pytest\\test_failures\\'

        for docx in os.listdir(path_to_folder):
            path_to_doc = os.path.join(path_to_folder, docx)
            pt_txt, _, _ = epilepsy_docx_to_txt(path_to_doc)
            pt_txt_anon_name, names = anonymise_name_txt(pt_txt, path_to_doc)


def test_failures_name_xml():  # ensure the many alternative regex and xml reading styles don't pick up names/DOB/MRNs where they shouldn't
    with pytest.raises(AttributeError):
        path_to_folder = 'L:\\word_docs\\pytest\\test_failures\\'

        for docx in os.listdir(path_to_folder):
            path_to_doc = os.path.join(path_to_folder, docx)
            pt_txt, _, _ = epilepsy_docx_to_txt(path_to_doc)
            pt_txt_anon_name, names = anonymise_name_txt(pt_txt, path_to_doc, xml=True)


