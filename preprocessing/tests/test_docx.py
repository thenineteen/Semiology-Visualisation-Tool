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
from ..json_keys_read import find_MRN_label_outcomes, outcomes_count
from ...crosstab.outcomes import gold_outcomes_MRNs

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
                     clean=False, save_path_anon="L:\\word_docs\\pytest\\test_texxts\\",
                     json_dictionary_file = 'L:\\word_docs\\pytest\\test_keys_single.json',
                     DOCX=True,
                     docx_to_txt_save_path="L:\\word_docs\\pytest\\docx_to_txt\\",
                     docx_xml_to_txt_save_path="L:\\word_docs\\pytest\\docx_xml_to_txt\\")

    with open ('L:\\word_docs\\pytest\\test_keys_single.json') as tk:
        test_json_data = json.load(tk)
    fixture = read_fixture(filename='fixture_anonymise_single.json')

    assert test_json_data == fixture


def test_skipNeurophysVTreports_and_anonnamexmlTrue():
    path_to_folder = 'L:\\word_docs\\pytest\\test_anon_name_xml_True\\'
    main_docx_preprocess(path_to_folder, read_tables=False,
                        clean=False, save_path_anon="L:\\word_docs\\pytest\\test_texxts\\",
                        json_dictionary_file = 'L:\\word_docs\\pytest\\test_keys.json',
                        DOCX=True,
                        docx_to_txt_save_path="L:\\word_docs\\pytest\\docx_to_txt\\",
                        docx_xml_to_txt_save_path="L:\\word_docs\\pytest\\docx_xml_to_txt\\")
    
    with open ('L:\\word_docs\\pytest\\test_keys.json') as tk:
        test_json_data = json.load(tk)
    fixture = read_fixture(filename='fixture_name_anon_xml_True.json')

    assert test_json_data == fixture


def test_write_MRN_from_filename_to_topoftxt():
    # run the scripts on the folder:
    path_to_folder = 'L:\\word_docs\\pytest\\test_write_MRN_from_filename_to_topoftxt\\'
    main_docx_preprocess(path_to_folder, read_tables=False,
                        clean=False, save_path_anon="L:\\word_docs\\pytest\\test_texxts_MRNtopoffile\\",
                        json_dictionary_file = 'L:\\word_docs\\pytest\\test_write_MRN_from_filename_to_topoftxt.json',
                        DOCX=True,
                        docx_to_txt_save_path="L:\\word_docs\\pytest\\docx_to_txt\\",
                        docx_xml_to_txt_save_path="L:\\word_docs\\pytest\\docx_xml_to_txt\\")

    # open the json dict and get all the keys:
    # read the first line of the .txt file and assert it is same as above:
    with open('L:\\word_docs\\pytest\\test_write_MRN_from_filename_to_topoftxt.json') as f:
        data = json.load(f)
        path_to_txt_folder = "L:\\word_docs\\pytest\\test_texxts_MRNtopoffile\\"
        for key, txt_file in zip(data.keys(), os.listdir(path_to_txt_folder)):
            uuid_no = key
            uuid_no_message = 'XXX pseudo_anon_dict_DOCX ' + str(uuid_no) + ' XXX'

            path_to_doc = os.path.join(path_to_txt_folder, txt_file)
            with open(path_to_doc, 'r') as txt_f:
                first_line = txt_f.readline()

            assert first_line.strip() == uuid_no_message


def test_MRN_funny(path_to_folder = 'L:\\word_docs\\pytest\\test_MRN_funny\\'):

    main_docx_preprocess(path_to_folder, read_tables=False,
                        clean=False, save_path_anon="L:\\word_docs\\pytest\\test_texxts_MRN_funny\\",
                        json_dictionary_file = 'L:\\word_docs\\pytest\\test_MRN_funny.json',
                        DOCX=True,
                        docx_to_txt_save_path="L:\\word_docs\\pytest\\docx_to_txt\\",
                        docx_xml_to_txt_save_path="L:\\word_docs\\pytest\\docx_xml_to_txt\\")

    with open('L:\\word_docs\\pytest\\test_MRN_funny.json') as f:
        data = json.load(f)
    fixture = read_fixture(filename='fixture_MRN_funny.json')

    assert data == fixture



def test_complex_DOB(path_to_folder = 'L:\\word_docs\\pytest\\test_complex_DOB\\'):
    # due to the order of MRN then DOB anonymisation in main_docx_preprocess, the third file here actually tests correct MRN anon
    # if fails, could be that instead of hosp no 12345678 it is 34567812 where 12 is the dd from DOB
    main_docx_preprocess(path_to_folder, read_tables=False,
                        clean=False, save_path_anon="L:\\word_docs\\pytest\\test_texxts_complex_DOB\\",
                        json_dictionary_file = 'L:\\word_docs\\pytest\\test_complex_DOB.json',
                        DOCX=True,
                        docx_to_txt_save_path="L:\\word_docs\\pytest\\docx_to_txt\\",
                        docx_xml_to_txt_save_path="L:\\word_docs\\pytest\\docx_xml_to_txt\\")

    with open('L:\\word_docs\\pytest\\test_complex_DOB.json') as f:
        data = json.load(f)
    fixture = read_fixture(filename='fixture_complex_DOB.json')

    assert data == fixture


def outcomes_tesT_factor(path_to_folder = 'L:\\word_docs\\pytest\\test_outcome_Gold',
                  save_path_anon="L:\\word_docs\\pytest\\test_texxts_outcomes\\",
                  temp_json = 'L:\\word_docs\\pytest\\outcomes_temp_G.json',
                  docx_to_txt_save_path="L:\\word_docs\\pytest\\docx_to_txt\\",
                  docx_xml_to_txt_save_path="L:\\word_docs\\pytest\\docx_xml_to_txt\\",
                  save_new_json_dict = "L:\\word_docs\\pytest\\test_outcomes_gold.json",
                  fixture_filename = 'fixture_outcomes_gold.json' ):

    # first convert .docx to .txt and anonymise and extract keys to MRNs:
    main_docx_preprocess(path_to_folder, read_tables=False,
                        clean=False, save_path_anon=save_path_anon,
                        json_dictionary_file=temp_json,
                        DOCX=True,
                        docx_to_txt_save_path=docx_to_txt_save_path,
                        docx_xml_to_txt_save_path=docx_xml_to_txt_save_path)
    
    # now get the outcomes from crosstab:
    gold_outcomes, had_surgery = gold_outcomes_MRNs()

    # now add the outcomes to the .json file:
    sensitive_data_outcomes = find_MRN_label_outcomes(gold_outcomes, had_surgery,
                              json_file_to_use = temp_json,
                              save_new_json_dict=save_new_json_dict)
    
    with open(save_new_json_dict) as f:
        data = json.load(f)
    fixture = read_fixture(filename=fixture_filename)

    return data, fixture


def test_outcomes_gold():
    data, fixture = outcomes_tesT_factor()
    assert data == fixture



def test_outcomes_resection(): # why do the DOB's not show up??
    
    data, fixture = outcomes_tesT_factor(path_to_folder = 'L:\\word_docs\\pytest\\test_outcome_resections',
                                         temp_json = 'L:\\word_docs\\pytest\\outcomes_temp_R.json',
                                         save_new_json_dict = "L:\\word_docs\\pytest\\test_outcomes_resections.json",
                                         fixture_filename = 'fixture_outcomes_resections.json',)
    
    assert data == fixture



def test_outcomes_no_surgery():
    
    data, fixture = outcomes_tesT_factor(path_to_folder = 'L:\\word_docs\\pytest\\test_outcome_no_surgery',
                                         temp_json = 'L:\\word_docs\\pytest\\outcomes_temp_N.json',
                                         save_new_json_dict = "L:\\word_docs\\pytest\\test_outcomes_no_resections.json",
                                         fixture_filename = 'fixture_outcomes_no_surgery.json',)
    
    assert data == fixture



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


@pytest.mark.xfail
def test_yet_to_fix(path_to_folder = 'L:\\word_docs\\pytest\\test_xfail\\'):

    main_docx_preprocess(path_to_folder, read_tables=False,
                        clean=False, save_path_anon="L:\\word_docs\\pytest\\empty\\",
                        json_dictionary_file = 'L:\\word_docs\\pytest\\test_xfail.json',
                        DOCX=True,
                        docx_to_txt_save_path="L:\\word_docs\\pytest\\docx_to_txt\\",
                        docx_xml_to_txt_save_path="L:\\word_docs\\pytest\\docx_xml_to_txt\\")

    with open('L:\\word_docs\\pytest\\test_xfail.json') as f:
        data = json.load(f)
    fixture = read_fixture(filename='fixture_xfail.json')

    assert data == fixture