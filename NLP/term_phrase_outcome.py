# use a term or semiology to find the files it occurs in and find the outcomes of those files it occurs in. 
# also print outcomes of files which the term doesn't occur in for comparison e.g. for a frequency chi-sq test

import re
import json

from NLP.b_1_filter_and_tokenise import *
from NLP.c_stemming import *

from crosstab.outcomes import *


def term_phrase_outcome(
    term_or_precise_phrase, # ensure term exists in the files e.g. don't use a full word on stemmed texts
    path_to_folder,  # files to look in for the term
    outcomes_json_file_specified=False,
    stemmed=False):

    rtf_origin=False
    no_file = 0

    no_Gold = 0
    no_Resections = 0
    no_No_Surgery = 0

    freq_in_all_files = 0


    for txt_file in os.listdir(path_to_folder):

        path_to_doc = os.path.join(path_to_folder, txt_file)
        
        #open the file
        pt_txt = open_txt_file(path_to_doc) # string output
        no_file += 1
        #search for the term: if not found, move to next file
        if not re.search(term_or_precise_phrase, pt_txt):
            continue
        
        else:   # found the term_or_phrase in this file. now identify the file.
            if stemmed:  
                # use the stemmed version of the pseudoanon document identifier uuid_no
                pseudo_anon = r"xxx pseudoanondictdocx (\d{1,4}) (?=xxx)"
            if not stemmed:   
                # use the normal DOCX pseudo anon uuid_no expression
                pseudo_anon = r"XXX pseudo_anon_dict_DOCX (\d{1,4}) (?=XXX)"



        if re.search(pseudo_anon, pt_txt): # must be DOCX file
            rtf_origin=False

        elif not re.search(pseudo_anon, pt_txt):  # then we know it is NOT a DOCX original file
            rtf_origin = True
            if stemmed:  
                 # use the stemmed version of the pseudoanon document identifier uuid_no
                pseudo_anon = r"xxx pseudoanondictrtf (\d{1,4}) (?=xxx)"
            else:   
                # use the normal pseudo anon uuid_no expression
                pseudo_anon = r"XXX pseudo_anon_dict_RTF (\d{1,4}) (?=XXX)"
            
        try:
            uuid_no = re.search(pseudo_anon, pt_txt)
            uuid_no = uuid_no.group().split()[-1]
        except AttributeError:
            print("AttributeError in file {} rtf_origin status: {}".format(txt_file, rtf_origin))
            continue  # skip this file but don't reverse counting the file no_file


            # TRY TO FIND FREQ OF OCCURANCE IN THIS FILE TOO:
        findall_term = re.findall(term_or_precise_phrase, pt_txt)
        findall_term = list(findall_term)
        freq_term_in_this_file = len(findall_term)
        freq_in_all_files = freq_in_all_files + freq_term_in_this_file



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
        if outcome=="No surgery":
            no_No_Surgery += 1
        elif outcome=="Resection":
            no_Resections += 1
        elif outcome=="Gold ILAE 1":
            no_Gold += 1
        
        # end of for loop through files




    # get list of all outcomes from crosstab
    gold_outcomes_list, had_surgery_MRNs = gold_outcomes_MRNs()
    total_Gold = len(gold_outcomes_list) # number of patients with Gold outcome from crosstab
    total_resection = len(had_surgery_MRNs)
    #total_no_resection = no_file - total_Gold - total_resection

    # print results
    total_number_occurances = no_Gold + no_Resections + no_No_Surgery
    print("number of files = {}".format(no_file))
    print("this term \"{}\" occurs in {} out of {} of the files (total of {} occurances)".format(term_or_precise_phrase, total_number_occurances, no_file, freq_in_all_files))
    print("\n{} times in patients with Gold ILAE 1 outcome. Number of all Gold patients {}".format(no_Gold, total_Gold))
    print("{} times in patients with Resections otherwise. Out of Total number of Resections {}".format(no_Resections, total_resection))
    print("{} times in patients with no surgery.".format(no_No_Surgery))
    print("\nfreq analysis: {} in Gold vs {} in non Gold".format(no_Gold, no_No_Surgery+no_Resections))
    return (no_file, no_Gold, no_Resections, no_No_Surgery, freq_in_all_files)