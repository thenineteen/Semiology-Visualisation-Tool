import json

def find_MRN_label_outcomes(list_MRNs_surgery_ILAE_1_all_follow_up_years,
             list_MRNs_surgery_not_gold_standard,
             json_file_to_use = "L:\\word_docs\\word_keys2.json",
             save_new_json_dict = "L:\\word_docs\\word_keys_outcomes.json"):

    """
    Opens the word_keys.json file containing a dictionary of sensitive data.
    Searches for specified MRNs, adds mdt/surgery outcome: 
        Gold, had surgery or no surgery.

    >list_MRNs: list of pre-specified MRNs.

    use like this:
    gold_outcomes_MRNs = ['QSD123456', '12345678'... etc]
    gold_outcomes_MRNs is same as first argument for this function
    had_surgery = ['hosp no pt 1', 'MRN for pt 2'... etc]
    sensitive_data_outcomes = find_MRN_label_outcomes(Gold_MRNs, had_surgery)
    """
    # open json key
    with open(json_file_to_use) as f:
        sensitive_data = json.load(f)

# for testing and creating list of MRNs:
    # had_surgery = []
    # for pseudo_anon_key in sensitive_data.keys():
    #     if int(pseudo_anon_key) > 5 and int(pseudo_anon_key)<15:
    #         surgery.append(sensitive_data[pseudo_anon_key][MRN])

    # loop through all keys    
    for pseudo_anon_key in sensitive_data.keys():
        
        # label gold standard outcomes
        if sensitive_data[pseudo_anon_key]['MRN'] in list_MRNs_surgery_ILAE_1_all_follow_up_years:
            sensitive_data[pseudo_anon_key]['MDT_Surgery_Outcome'] = "Gold ILAE 1"

        # label surgical resection without gold standard outcomes
        elif sensitive_data[pseudo_anon_key]['MRN'] in list_MRNs_surgery_not_gold_standard:
            sensitive_data[pseudo_anon_key]['MDT_Surgery_Outcome'] = "Resection"
        
        else:
            sensitive_data[pseudo_anon_key]['MDT_Surgery_Outcome'] = "No surgery"

    with open(save_new_json_dict, 'w') as file:

                file.seek(0)  # rewind

                json.dump(sensitive_data, file)
                #file.write(json.dumps(pseudo_anon_dict))

                file.truncate()

    return sensitive_data


def outcomes_count(json_file = "L:\\word_docs\\RTF_done\\3.5 RTF_keys_outcomes.json"):
    """
    Give this function the .json file key with outcomes, and it will count number of outcomes
    in this key for 'Gold ILAE 1', 'Resection' and 'No surgery'
    """
    with open(json_file) as f:
        rtf_keys = json.load(f)

    m = 0
    n = 0
    o = 0
    for pseudoanonkey in rtf_keys.keys():
        if rtf_keys[pseudoanonkey]['MDT_Surgery_Outcome'] == 'Gold ILAE 1':
            m += 1
            print (pseudoanonkey, rtf_keys[pseudoanonkey])
        if rtf_keys[pseudoanonkey]['MDT_Surgery_Outcome'] == 'Resection':
            n += 1
        if rtf_keys[pseudoanonkey]['MDT_Surgery_Outcome'] == 'No surgery':
            o += 1
    print('Gold ILAE 1 = \t\t{}'.format(m))
    print('Resection = \t\t{}'.format(n))
    print('No surgery = \t\t{}'.format(o))
