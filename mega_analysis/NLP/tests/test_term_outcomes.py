import yaml
import re
from ..term_phrase_outcome import term_phrase_outcome
from ..term_phrase_outcome_cycle_many_terms import *
from ..term_phrase_negation_second_pass import *
from .view_results_prior_to_negation import *



def test_term_phrase_outcome():
    """
    cycle_semiology_terms uses case insensitive regex whereas term_phrase_outcome is case sensitive
    """

    term_or_precise_phrase, no_file, freq_in_all_files, \
    no_Gold, no_Resections, no_No_Surgery,\
    no_Gold_absent_term, no_Resections_absent_term, no_No_Surgery_absent_term= \
        term_phrase_outcome(
            r"([eE][pP][iI][gG])|([aA][bB][dD][oO])", 
            path_to_folder="L:\\word_docs\\NLP\\both_done_copy\\", 
            stemmed=False,
            suppress_print_cycle=False,
            positive_files=[])
    
    assert (
        term_or_precise_phrase, no_file, freq_in_all_files, \
        no_Gold, no_Resections, no_No_Surgery,\
        no_Gold_absent_term, no_Resections_absent_term, no_No_Surgery_absent_term) ==\
        ('([eE][pP][iI][gG])|([aA][bB][dD][oO])', 1209, 440,
         65, 55, 142,
         122, 262, 562)



def test_cycle_semiology_terms(
    path_to_yaml_file = 'C:\\Users\\ali_m\\AnacondaProjects\\PhD\\Epilepsy_Surgery_Project\\NLP\\tests\\semiology_dictionary.yaml',
    semiology_key = "epigastric",
    path_to_folder_ = "L:\\word_docs\\NLP\\tests\\cycle_semiology_terms\\"):
    """
    tests that each semiology_key is counted only once as being present in a file, no matter how many of 
    its value semiology_terms are present. 
    cycle_semiology_terms uses case insensitive regex whereas term_phrase_outcome is case sensitive
    """
    
    no_file, freq_in_all_files_semiology,\
    Gold_semiology,\
    Resections_semiology,\
    No_Surgery_semiology,\
    Gold_absent_term_semiology,\
    Resections_absent_term_semiology,\
    No_Surgery_absent_term_semiology = \
        cycle_semiology_terms(path_to_yaml_file, semiology_key, path_to_folder_)

    assert Gold_semiology+Resections_semiology+No_Surgery_semiology+\
           Gold_absent_term_semiology+Resections_absent_term_semiology+No_Surgery_absent_term_semiology==no_file



def test_cycle_semiology_terms_all_files(
    path_to_yaml_file = 'C:\\Users\\ali_m\\AnacondaProjects\\PhD\\Epilepsy_Surgery_Project\\NLP\\tests\\semiology_dictionary.yaml',
    semiology_key = "epigastric",
    path_to_folder_ = "L:\\word_docs\\NLP\\both_done_copy\\"):
    """
    tests that each semiology_key is counted only once as being present in a file, no matter how many of 
    its value semiology_terms are present. 
    cycle_semiology_terms uses case insensitive regex whereas term_phrase_outcome is case sensitive
    """
    
    no_file, freq_in_all_files_semiology,\
    Gold_semiology,\
    Resections_semiology,\
    No_Surgery_semiology,\
    Gold_absent_term_semiology,\
    Resections_absent_term_semiology,\
    No_Surgery_absent_term_semiology = \
        cycle_semiology_terms(path_to_yaml_file, semiology_key, path_to_folder_)

    assert (Gold_semiology+Resections_semiology+No_Surgery_semiology+\
           Gold_absent_term_semiology+Resections_absent_term_semiology+No_Surgery_absent_term_semiology,\
           Gold_semiology+Resections_semiology+No_Surgery_semiology,\
           ==\
           (no_file, 
           )
    )





def test_view_results_prior_to_negation_second_pass_simple(
    term_or_precise_phrase=r"([eE][pP][iI][gG])|([aA][bB][dD][oO])", 
    path_to_folder="L:\\word_docs\\NLP\\tests\\term_negation\\"):
    """
    This just calls the term_phrase_outcome() with more unpacked returns
    This is case sensitive
    """

    term_or_precise_phrase, no_file, freq_in_all_files, \
    no_Gold, no_Resections, no_No_Surgery,\
    no_Gold_absent_term, no_Resections_absent_term, no_No_Surgery_absent_term,\
    positive_files, negative_files,\
    list_of_search_group, list_of_findall, list_of_file_outcomes =\
        view_results_prior_to_negation_second_pass(
            term_or_precise_phrase, # ensure term exists in the files e.g. don't use a full word on stemmed texts
            path_to_folder,  # files to look in for the term
            outcomes_json_file_specified=False,
            stemmed=False,
            suppress_print_cycle=False,
            term_phrase_negation_second_pass_=True)




    assert (
        no_file, freq_in_all_files, \
        no_Gold, no_Resections, no_No_Surgery,\
        no_Gold_absent_term, no_Resections_absent_term, no_No_Surgery_absent_term,\
        (no_Gold + no_Resections + no_No_Surgery) ==\
        (4, 3,
         1, 1, 1,
         0, 1, 0, len(list_of_findall)))






# def test_term_phrase_negation_second_pass_proper(
#     path_to_yaml_file = 'C:\\Users\\ali_m\\AnacondaProjects\\PhD\\Epilepsy_Surgery_Project\\NLP\\tests\\semiology_dictionary.yaml',
#     semiology_key = "epigastric",
#     path_to_folder_ = "L:\\word_docs\\NLP\\tests\\cycle_semiology_terms_NLA\\"):

#     no_file, freq_in_all_files_semiology,\
#     Gold_semiology,\
#     Resections_semiology,\
#     No_Surgery_semiology,\
#     Gold_absent_term_semiology,\
#     Resections_absent_term_semiology,\
#     No_Surgery_absent_term_semiology = \
#         cycle_semiology_terms(path_to_yaml_file, semiology_key, path_to_folder_)

#     if (Gold_semiology == 1 and
#         Resections_semiology == 2 and\
#         No_Surgery_semiology == 3 and\
#         Gold_absent_term_semiology == 4 and\
#         Resections_absent_term_semiology == 5 and\
#         No_Surgery_absent_term_semiology == 6):
#         correct=True
    
#     else:
#         correct=False

#     assert correct==True
    
