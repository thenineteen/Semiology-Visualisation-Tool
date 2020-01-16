import re
import json

try: 
    from crosstab.outcomes_by_resected_lobe import *
    from preprocessing.word_preprocess import save_as_txt
except:
    from ..crosstab.outcomes_by_resected_lobe import *
    from ..preprocessing.word_preprocess import save_as_txt


def specific_lobe_resections(path_to_folder, 
                            lobes_to_use=['T Lx', 'T Lesx'], 
                            stemmed=False,
                            save_path='"L:\\word_docs\\NLP\\TEMPORAL_RESECTIONS\\'):
    """
    Use the outcomes_by_resected_lobe function to copy files into a new folder.
    """

    if not lobes_to_use:
        print('please specify lobes of interest - see outcomes_by_resected_lobe docstring for list')
        return

    else:
    # make a list of all the MRNs of patients with resections involving the temporal lobe
        temporal_gold_outcomes_MRNs, temporal_had_surgery_MRNs =\
            outcomes_by_resected_lobe(directory='L:\\', filename='All_Epilepsy_Ops_CROSSTAB_Statistics_YAY_2019.xlsx',
                                    lobes=lobes_to_use)
    

    # initialise
    no_file = 0
    no_temporal_gold = 0
    no_temporal_nongold = 0

    
    # open each file and read the pseudo_anon_key: copy from term_phrase_outcome:

    for txt_file in os.listdir(path_to_folder):

        path_to_doc = os.path.join(path_to_folder, txt_file)
        
        #open the file
        with open(path_to_doc, 'r') as f:
            pt_txt = f.read()
        no_file += 1

        # Identify the file
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
            print("Pseudo_anon uuid AttributeError in file {} rtf_origin status: {}".format(txt_file, rtf_origin))
            continue  # skip this file but don't reverse counting the file no_file







    # check the pseudo_anon_key's corresponding MRN from the json dict
        if rtf_origin:
            json_file = 'L:\\word_docs\\NLP\\5 word_RTF_keys_12_13_14_manual_outcomes_exclude_no_outcomes.json'
        else:
            json_file = 'L:\\word_docs\\NLP\\5 manually_handled_keys_outcomes_edited_exclude_no_outcomes.json'
            
        with open(json_file) as f:
            data=json.load(f)

        try:
            MRN = data[str(uuid_no)]['MRN']
        except KeyError:
            print("KeyError for {} in {}. rtf_origin status is: {}".format(uuid_no, txt_file, rtf_origin))
            continue  # skip this file but don't reverse counting the file no_file






    # check if the MRN is in any of above two temporal lists: temporal_gold_outcomes_MRNs, temporal_had_surgery_MRNs
    # if it is in the any of the lists, then save the text in a new folder. Otherwise continue

        if MRN in temporal_gold_outcomes_MRNs:
            no_temporal_gold += 1
        elif MRN in temporal_had_surgery_MRNs:
            no_temporal_nongold +=1
        else:
            continue # skip this file

        
        
        save_filename = path_to_doc.split("\\")[-1]
        complete_filename = os.path.join(save_path, save_filename)       
        with open(complete_filename, "w", errors='backslashreplace') as f:
            f.write(pt_txt)





    print('files in folder: {}'.format(no_file))
    print('temporal gold outcomes: {}'.format(no_temporal_gold))
    print('temporal nongold: {}'.format(no_temporal_nongold))

    return
