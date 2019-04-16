import re
try:
    from NLP.term_phrase_outcome import *
    from NLP.tests.semiology_negations import *
except:
    from .term_phrase_outcome import *
    from .tests.semiology_negations import *

NLA, NLB = semiology_negations()

def term_phrase_negation_second_pass(
    term_or_precise_phrase, # ensure term exists in the files e.g. don't use a full word on stemmed texts
    path_to_folder,  # files to look in for the term
    outcomes_json_file_specified=False,
    stemmed=False,
    suppress_print_cycle=False,
    term_phrase_negation_second_pass_=True):
    """
    After term_phrase_outcome(), finds the matches and prints them.
    After inspection of results, objective was to 
    
        (add the negation sentences ("no epigastric aura" "denies rising abdominal aura") 
        to semiology_negations. Then use this function to remove these and reverse the counts. 
        - Preferably intergrate into the cycle_many_terms function but maybe hard.
        Ensure no positive in the negatives phrases)

    But easier to just visually inspect printouts and alter the dataframe /excel file manually. 


    """
    term_or_precise_phrase = r"(?i).*" + term_or_precise_phrase + r".*"
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

    findall_counter = -1
    negative_counter = -1

    for findall_result in list_of_findall:
        findall_counter += 1
        for negative_phrase in NLB:
            if re.search(re.compile(negative_phrase), findall_result):
            # found match so need to remove this result
                
                file_with_negation_outcome = list_of_file_outcomes[findall_counter]
                outcome = file_with_negation_outcome
                
                if outcome=="No surgery":
                    no_No_Surgery -= 1
                elif outcome=="Resection":
                    no_Resections -= 1
                elif outcome=="Gold ILAE 1":
                    no_Gold -= 1


    return(term_or_precise_phrase, no_file, freq_in_all_files, \
            no_Gold, no_Resections, no_No_Surgery,\
            no_Gold_absent_term, no_Resections_absent_term, no_No_Surgery_absent_term,
            positive_files, negative_files,
            list_of_search_group, list_of_findall, list_of_file_outcomes)