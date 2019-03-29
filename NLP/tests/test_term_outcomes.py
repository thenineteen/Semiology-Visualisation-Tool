import yaml
import re
from ..term_phrase_outcome import term_phrase_outcome
from ..term_phrase_outcome_cycle_many_terms import term_phrase_outcome_cycle_semiology_fixture



def test_term_phrase_outcome():
    term_or_precise_phrase, no_file, freq_in_all_files, \
    no_Gold, no_Resections, no_No_Surgery,\
    no_Gold_absent_term, no_No_Surgery_absent_term, no_Resections_absent_term= \
    term_phrase_outcome(
        r"([eE][pP][iI][gG])|([aA][bB][dD][oO])", 
        path_to_folder="L:\\word_docs\\NLP\\both_done_copy\\", 
        stemmed=False,
        suppress_print_cycle=False,
        positive_files=[])
    
    assert (
        term_or_precise_phrase, no_file, freq_in_all_files, \
        no_Gold, no_Resections, no_No_Surgery,\
        no_Gold_absent_term, no_No_Surgery_absent_term, no_Resections_absent_term) ==\
        ('([eE][pP][iI][gG])|([aA][bB][dD][oO])', 1209, 440,
         65, 55, 142,
         122, 562, 262)



# def test_semiology_fixture():
#     # load the fixtyres.yaml file: yaml_file
#     yaml_file = yaml.load(open('C:\\Users\\ali_m\\AnacondaProjects\\PhD\\Epilepsy_Surgery_Project\\NLP\\tests\\semiology_dictionary.yaml'))
#     path_to_folder="L:\\word_docs\\NLP\\tests\\"

#     term_phrase_outcome_cycle_semiology_fixture(yaml_file, path_to_folder)
