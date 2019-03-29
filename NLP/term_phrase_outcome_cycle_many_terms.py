

import yaml
import re
try:
    from NLP.term_phrase_outcome import *
except:
    from .term_phrase_outcome import *

def term_phrase_outcome_cycle_semiology_fixture(
    path_to_yaml_file = 'C:\\Users\\ali_m\\AnacondaProjects\\PhD\\Epilepsy_Surgery_Project\\NLP\\tests\\semiology_dictionary.yaml',
    path_to_folder_="L:\\word_docs\\NLP\\tests\\"):
    
    """
    Cycle through many terms and run term_phrase_outcome.py
    Also use this for the pytest
    """

    # load the fixtyres.yaml file: yaml_file
    yaml_file = yaml.load(open(path_to_yaml_file))

    positive_files_cycle = []  # initialise, updates later when running term_phrase_outcome()
    negative_files_cycle = []
    semiology_counts = {}

    # cycle through the revelant dictionary keys (lists in yaml file)
    for semiology_key in yaml_file['semiology']['auras']:
        
        # initialise
        no_Gold_semiology_dict = 0
        no_Resections_semiology_dict = 0
        no_No_Surgery_semiology_dict = 0
        freq_in_all_files_semiology_dict = 0 # number of repetitions across all files

        # initialise the counters for file outcomes in the specified folder 
        no_No_Surgery_absent_term_semiology_dict = 0
        no_Resections_absent_term_semiology_dict = 0
        no_Gold_absent_term_semiology_dict = 0


        # cycle through the list of equivalent semiology terms
        for semiology_term in yaml_file['semiology']['auras'][semiology_key]:
            semiology_term_caseins = r"(?i)" + semiology_term   # lower case regex
            term_or_precise_phrase = re.compile(semiology_term_caseins)

            (t_or_p_ph, no_file, freq_in_all_files, \
            no_Gold, no_Resections, no_No_Surgery,\
            no_Gold_absent_term, no_No_Surgery_absent_term, no_Resections_absent_term,
            positive_files_cycle) = \
            term_phrase_outcome(
                term_or_precise_phrase, # ensure term exists in the files e.g. don't use a full word on stemmed texts
                path_to_folder=path_to_folder_,  # files to look in for the term
                outcomes_json_file_specified=False,
                stemmed=False,  # use original files - ensure folder above matches and is not a stemmed version of the files
                suppress_print_cycle=True,
                positive_files=positive_files_cycle,
                negative_files=negative_files_cycle)  # suppress prints as need to collate data for all the terms when cycling through equivalent terms

        
            # update all counts after each equivalent term
            no_Gold_semiology_dict += no_Gold
            no_Resections_semiology_dict += no_Resections
            no_No_Surgery_semiology_dict += no_No_Surgery
            freq_in_all_files_semiology_dict +=  freq_in_all_files # number of repetitions across all files
            no_Gold_absent_term_semiology_dict += no_Gold_absent_term
            no_Resections_absent_term_semiology_dict += no_Resections_absent_term
            no_No_Surgery_absent_term_semiology_dict += no_No_Surgery_absent_term


        return_tuple = (no_file, freq_in_all_files_semiology_dict,\
                        no_Gold_semiology_dict,\
                        no_Resections_semiology_dict,\
                        no_No_Surgery_semiology_dict,\
                        no_Gold_absent_term_semiology_dict,\
                        no_Resections_absent_term_semiology_dict,\
                        no_No_Surgery_absent_term_semiology_dict)
    
        semiology_counts[semiology_key] = (return_tuple)



    # end of cycle through list of equivalent terms for one semiology
    
    
    return (semiology_counts)
