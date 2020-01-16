import re
import os
try:
    from NLP.term_phrase_outcome import *
except:
    from .term_phrase_outcome import *


def view_results_prior_to_negation_second_pass(
    term_or_precise_phrase, # ensure term exists in the files e.g. don't use a full word on stemmed texts
    path_to_folder,  # files to look in for the term
    outcomes_json_file_specified=False,
    stemmed=False,
    suppress_print_cycle=False,
    term_phrase_negation_second_pass_=True):
    """
    After term_phrase_outcome(), finds the matches and prints them.
    After inspection of results, add the negation sentences ("no epigastric aura" "denies rising abdominal aura") 
        to semiology_negations.
    Then use term_phrase_negation_second_pass function to remove these and reverse the counts.

    Similar to regex_read_entire_match_line but that uses one amalgamated file of entire corpus so difficult to use for pytest initially. 
    """

    term_or_precise_phrase = r"(?i)" + r".*" + term_or_precise_phrase + r".*"
    term_or_precise_phrase, no_file, freq_in_all_files, \
    no_Gold, no_Resections, no_No_Surgery,\
    no_Gold_absent_term, no_Resections_absent_term, no_No_Surgery_absent_term,\
    positive_files, negative_files,\
    list_of_search_group, list_of_findall, list_of_file_outcomes =\
        term_phrase_outcome(
            term_or_precise_phrase, # ensure term exists in the files e.g. don't use a full word on stemmed texts
            path_to_folder,  # files to look in for the term
            outcomes_json_file_specified=False,
            stemmed=False,
            suppress_print_cycle=False,
            term_phrase_negation_second_pass_=True) # extra return tuples


    #print("list_of_search_group: {}".format(list_of_search_group))
    for result in list_of_findall:
        print("\n~~~~~~~~~~~~~\nlist_of_findall: {}".format(result))
    print("\n\nlist_of_file_outcomes: {}".format(list_of_file_outcomes))

    return(term_or_precise_phrase, no_file, freq_in_all_files, \
            no_Gold, no_Resections, no_No_Surgery,\
            no_Gold_absent_term, no_Resections_absent_term, no_No_Surgery_absent_term,
            positive_files, negative_files,
            list_of_search_group, list_of_findall, list_of_file_outcomes)