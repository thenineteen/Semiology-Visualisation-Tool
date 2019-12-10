

import yaml
import re
try:
    from NLP.term_phrase_outcome import *
    #from NLP.tests.semiology_lookarounds import *
except:
    from .term_phrase_outcome import *
    #from .tests.semiology_lookarounds import *


def cycle_semiology_terms(path_to_yaml_file, semiology_key, path_to_folder_):
    """cycle through the list of equivalent/synonymous semiology terms
    Update the line 
    "for semiology_term in yaml_file['semiology']['motor']['automatisms'][semiology_key]" to relevant keys
        only change the keys prior to [semiology_key]
    """

    # initialise term_present (=positive_files) and negatives folders
    # they update when running term_phrase_outcome()
    positive_files_cycle = []
    negative_files_cycle = []
    Gold_semiology = 0
    Resections_semiology = 0
    No_Surgery_semiology = 0
    freq_in_all_files_semiology = 0 # number of repetitions across all files
    Gold_absent_term_semiology = 0
    Resections_absent_term_semiology = 0
    No_Surgery_absent_term_semiology = 0
    
    # open yaml semiology_keys/terms
    yaml_file = yaml.load(open(path_to_yaml_file))

    ## open .py semiology_lookarounds to go with the above yaml: defunct as un maintainable, use semiology_negations instead
    #NLA, NLB = _semiology_lookarounds()

    # for semiology_term in yaml_file['semiology']['auras'][semiology_key]:
    # for semiology_term in yaml_file['semiology']['motor']['simple'][semiology_key]:
    # for semiology_term in yaml_file['semiology']['motor']['complex'][semiology_key]:
    for semiology_term in yaml_file['semiology']['motor']['automatisms'][semiology_key]:
    # for semiology_term in yaml_file['semiology']['speech'][semiology_key]:
    # for semiology_term in yaml_file['semiology']['consciousness'][semiology_key]:
    # for semiology_term in yaml_file[semiology_key]:  # use this for hippocampal sclerosis

        #semiology_term = NLB[semiology_key] + semiology_term
        semiology_term_caseins = r"(?i)" + semiology_term   # lower case regex
        term_or_precise_phrase = re.compile(semiology_term_caseins)

        (t_or_p_ph, no_file, freq_in_all_files_semiology, \
        Gold_semiology, Resections_semiology, No_Surgery_semiology,\
        Gold_absent_term_semiology, Resections_absent_term_semiology, No_Surgery_absent_term_semiology,
        positive_files_cycle, negative_files_cycle) = \
        term_phrase_outcome(
            term_or_precise_phrase, # ensure term exists in the files e.g. don't use a full word on stemmed texts
            path_to_folder=path_to_folder_,  # files to look in for the term
            outcomes_json_file_specified=False,
            stemmed=False,  # use original files - ensure folder above matches and is not a stemmed version of the files
            suppress_print_cycle=True, # suppress prints as need to collate data for all the terms when cycling through equivalent terms
            positive_files=positive_files_cycle,
            negative_files=negative_files_cycle,
            no_Gold = Gold_semiology,
            no_Resections = Resections_semiology,
            no_No_Surgery = No_Surgery_semiology,
            freq_in_all_files = freq_in_all_files_semiology,
            no_Gold_absent_term = Gold_absent_term_semiology,
            no_Resections_absent_term = Resections_absent_term_semiology,
            no_No_Surgery_absent_term = No_Surgery_absent_term_semiology)  
    
        # # update all counts after each equivalent term
        # no_Gold_semiology_dict += no_Gold
        # no_Resections_semiology_dict += no_Resections
        # no_No_Surgery_semiology_dict += no_No_Surgery
        # freq_in_all_files_semiology_dict +=  freq_in_all_files # number of repetitions across all files
        # no_Gold_absent_term_semiology_dict += no_Gold_absent_term
        # no_Resections_absent_term_semiology_dict += no_Resections_absent_term
        # no_No_Surgery_absent_term_semiology_dict += no_No_Surgery_absent_term


        # end of cycle through list of equivalent semiology_terms for one semiology_key

    return_tuple = (no_file, freq_in_all_files_semiology,\
                    Gold_semiology,\
                    Resections_semiology,\
                    No_Surgery_semiology,\
                    Gold_absent_term_semiology,\
                    Resections_absent_term_semiology,\
                    No_Surgery_absent_term_semiology,\
                    positive_files_cycle, negative_files_cycle)

    return(return_tuple)






def cycle_semiology_keys():
    for semiology_key in yaml_file['semiology']['auras']:
        semiology_counts[semiology_key] = cycle_semiology_terms()



def term_phrase_outcome_cycle_semiology_fixture(
    path_to_yaml_file = 'C:\\Users\\ali_m\\AnacondaProjects\\PhD\\Epilepsy_Surgery_Project\\NLP\\tests\\semiology_dictionary.yaml',
    path_to_folder_="L:\\word_docs\\NLP\\tests\\"):
    
    """
    Cycle through many non-synonymous terms and run term_phrase_outcome.py
    Also use this for the pytest
    """

    # load the fixtyres.yaml file: yaml_file
    yaml_file = yaml.load(open(path_to_yaml_file))

    positive_files_cycle = []  # initialise, updates later when running term_phrase_outcome()
    negative_files_cycle = []
    semiology_counts = {}

    # cycle through the revelant dictionary keys (lists in yaml file)
    cycle_semiology_keys()

    # initialise
    no_Gold_semiology_dict = 0
    no_Resections_semiology_dict = 0
    no_No_Surgery_semiology_dict = 0
    freq_in_all_files_semiology_dict = 0 # number of repetitions across all files
    no_Gold_absent_term_semiology_dict = 0
    no_Resections_absent_term_semiology_dict = 0
    no_No_Surgery_absent_term_semiology_dict = 0


       

    return (semiology_counts)

