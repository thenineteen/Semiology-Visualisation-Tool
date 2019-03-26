# use a term or semiology to find the files it occurs in and find the outcomes of those files it occurs in. 
# also print outcomes of files which the term doesn't occur in for comparison e.g. for a frequency chi-sq test

import re
import json
from scipy.stats import chi2_contingency

from NLP.b_1_filter_and_tokenise import *
from NLP.c_stemming import *

from crosstab.outcomes import *


# def counter_file_outcome(json_file):
#     """
#     FACTOR STUB: count the outcomes of files in specified folder. 
#     Not completed/used yet.
#     """
#     with open(json_file) as f:
#         data=json.load(f)

#         outcome = data[str(uuid_no)]['MDT_Surgery_Outcome']


#     # now add outcome to list of their own
#     if outcome=="No surgery":
#         no_No_Surgery += 1
#     elif outcome=="Resection":
#         no_Resections += 1
#     elif outcome=="Gold ILAE 1":
#         no_Gold += 1

#     return sensitive_data








def term_phrase_outcome(
    term_or_precise_phrase, # ensure term exists in the files e.g. don't use a full word on stemmed texts
    path_to_folder,  # files to look in for the term
    outcomes_json_file_specified=False,
    stemmed=False):


    rtf_origin=False
    no_file = 0

    #initialise counters for term occurance in file based on outcome of that file
    no_Gold = 0
    no_Resections = 0
    no_No_Surgery = 0
    freq_in_all_files = 0 # number of repetitions across all files

    # initialise the counters for file outcomes in the specified folder 
    no_No_Surgery_absent_term = 0
    no_Resections_absent_term = 0
    no_Gold_absent_term = 0


    for txt_file in os.listdir(path_to_folder):

        path_to_doc = os.path.join(path_to_folder, txt_file)
        
        #open the file
        pt_txt = open_txt_file(path_to_doc) # string output
        no_file += 1
        
   
        # Identify the file (whether term exists or not in this file)
        # DOCX
        if stemmed:  
            # use the stemmed version of the pseudoanon document identifier uuid_no
            pseudo_anon = r"xxx pseudoanondictdocx (\d{1,4}) (?=xxx)"
        if not stemmed:   
            # use the normal DOCX pseudo anon uuid_no expression
            pseudo_anon = r"XXX pseudo_?anon_?dict_?DOCX (\d{1,4}) (?=XXX)"

        if re.search(pseudo_anon, pt_txt): # must be DOCX file
            rtf_origin=False

        elif not re.search(pseudo_anon, pt_txt):  # then we know it is NOT a DOCX original file
        # RTF
            rtf_origin = True
            if stemmed:  
                # use the stemmed version of the pseudoanon document identifier uuid_no
                pseudo_anon = r"xxx pseudoanondictrtf (\d{1,4}) (?=xxx)"
            else:   
                # use the normal pseudo anon uuid_no expression
                pseudo_anon = r"XXX pseudo_?anon_?dict_?RTF (\d{1,4}) (?=XXX)"
            
        try:
            uuid_no = re.search(pseudo_anon, pt_txt)
            uuid_no = uuid_no.group().split()[-1]
        
        except AttributeError:
            print("AttributeError in file {} rtf_origin status: {}".format(txt_file, rtf_origin))
            continue  # skip this file but don't reverse counting the file no_file


        # now check the outcome for this uuid_no
        # can use the json file with the outcomes or the original file
        # use json here

        if outcomes_json_file_specified:  # if user defined which json file to use, use that!
            json_file = outcomes_json_file_specified
        elif rtf_origin:
            json_file = 'L:\\word_docs\\NLP\\4.5 word_RTF_keys_12_13_14_manual_outcomes.json'
        else:
            json_file = 'L:\\word_docs\\NLP\\4 manually_handled_keys_outcomes_edited.json'
        
        with open(json_file) as f:
            data=json.load(f)

            try:
                outcome = data[str(uuid_no)]['MDT_Surgery_Outcome']
            except KeyError:
                print("KeyError for {} in {}. rtf_origin status is: {}".format(uuid_no, txt_file, rtf_origin))
                continue  # skip this file but don't reverse counting the file no_file

        # now add outcome to list of their own
       
        #search for the term: if not found, count the outcome of this term-non-occurance-file and then move to next file
        if not re.search(term_or_precise_phrase, pt_txt) and not re.search(term_or_precise_phrase, pt_txt.lower()):      
            if outcome=="No surgery":
                no_No_Surgery_absent_term += 1
            elif outcome=="Resection":
                no_Resections_absent_term += 1
            elif outcome=="Gold ILAE 1":
                no_Gold_absent_term += 1
            continue  # skip this file but don't reverse counting the file no_file

        elif re.search(term_or_precise_phrase, pt_txt):   # term is found in this file
            # FIND FREQ OF OCCURANCE IN THIS FILE TOO:
            findall_term = re.findall(term_or_precise_phrase, pt_txt)
            findall_term = list(findall_term)
            freq_term_in_this_file = len(findall_term)
            freq_in_all_files = freq_in_all_files + freq_term_in_this_file
            # check: should be able to replace freq above with nltk.FreqDist()

            if outcome=="No surgery":
                no_No_Surgery += 1
            elif outcome=="Resection":
                no_Resections += 1
            elif outcome=="Gold ILAE 1":
                no_Gold += 1
    
        elif re.search(term_or_precise_phrase, pt_txt.lower()): # in stemmed files this shouldn't make a difference. 
            print("Modify regex search term or phrase: lower case searches found {} term in file: {}".format(term_or_precise_phrase, txt_file))



        # end of for loop through files
        




    # get list of all outcomes from crosstab
    gold_outcomes_list, had_surgery_MRNs = gold_outcomes_MRNs()
    total_Gold = len(gold_outcomes_list) # number of *patients* with Gold outcome from crosstab
    total_resection = len(had_surgery_MRNs)
    #total_no_resection = no_file - total_Gold - total_resection

    # print results
    total_number_occurances = no_Gold + no_Resections + no_No_Surgery
    print("number of files = {}".format(no_file))
    print("this term \"{}\" occurs in {} out of {} of the files (total of {} occurances/repetitions)".format(term_or_precise_phrase, total_number_occurances, no_file, freq_in_all_files))
    print("\n{} times in files with Gold ILAE 1 outcome. {} Gold outcome files without this term. \n\t(Number of all Gold patients {})".format(no_Gold, no_Gold_absent_term, total_Gold))
    print("{} times in files with Resections otherwise. {} Resection outcome files without this term. \n\t(Number of all (non-Gold) Resections {})".format(no_Resections, no_Resections_absent_term, total_resection))
    print("{} times in files with no surgery. {} no surgery files without this term.".format(no_No_Surgery, no_No_Surgery_absent_term))
    print("\nfreq analysis: {} occurs {} in Gold files vs {} in non-Gold files".format(term_or_precise_phrase, no_Gold, no_No_Surgery + no_Resections))
    
    check_assertion = ((no_Gold + no_Gold_absent_term + no_No_Surgery + no_No_Surgery_absent_term + no_Resections + no_Resections_absent_term)==no_file )
    print("\ncheck assertion: {}".format(check_assertion))
    if check_assertion==False:
        print("\tno_Gold", no_Gold) 
        print("\tno_Gold_absent_term", no_Gold_absent_term) 
        print("\tno_No_Surgery", no_No_Surgery)
        print("\tno_No_Surgery_absent_term", no_No_Surgery_absent_term)
        print("\tno_Resections", no_Resections) 
        print("\tno_Resections_absent_term", no_Resections_absent_term)
        total_files = no_Gold+no_Gold_absent_term+no_No_Surgery+no_No_Surgery_absent_term+no_Resections+no_Resections_absent_term
        print("\t{} != {}".format(total_files, no_file))
    # pos_control = ((1+2)==3)
    # print("1+2 ==3 {}".format(pos_control))

    total_gold_files = no_Gold + no_Gold_absent_term
    print("\nproportion of Gold files with {} term = {}/{} = {}".format(term_or_precise_phrase, no_Gold, total_gold_files, round(no_Gold/total_gold_files,2) ))
    total_non_gold_files = no_No_Surgery + no_Resections + no_No_Surgery_absent_term + no_Resections_absent_term
    proportion_non_gold = round((no_No_Surgery+no_Resections)/total_non_gold_files,2)
    print("proportion of Non-Gold files with {} term = {}/{} = {}\n\n\n".format(term_or_precise_phrase, no_No_Surgery+no_Resections, total_non_gold_files, proportion_non_gold))



    

    # end of for loop through list of terms_phrases
    
    return(term_or_precise_phrase, no_file, freq_in_all_files, \
           no_Gold, no_Resections, no_No_Surgery,\
           no_Gold_absent_term, no_No_Surgery_absent_term, no_Resections_absent_term)
    #return (no_file, no_Gold, no_Resections, no_No_Surgery, freq_in_all_files)

    