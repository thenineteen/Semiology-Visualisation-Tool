import json
import pandas as pd
import re
import pickle

from crosstab.outcomes import*


def openpickle(path_to_file):
    with open(path_to_file, 'rb') as f:
        data = pickle.load(f)

    return data

_, had_surgery_MRNs = gold_outcomes_MRNs()
path_to_file2 = 'L:\\word_docs\\NLP\\Data Pickles\\gold_outcomes_list.pickle'
gold_outcomes_list = openpickle(path_to_file2)


def populate_main_dataframe(df, df_No_surgery,
                            positive_or_negative_files,
                            add_1_or_0,
                            semiology_key):

    """
    positive_or_negative_files: e.g.  Data_Epigastric['negative_files_cycle']. list of path_to_files
    add_1_or_0: if positive files, 1. If negative files, 0. integer
        RUN POSITIVES FIRST
    semiology_key: e.g. "Epigastric Aura"
    must already have a df and df_No_surgery 

    returns updated dataframes
    """


    # open the json pseudo anon keys for docx and rtfs:
    json_file_rtf = "L:\\word_docs\\NLP\\5 word_RTF_keys_12_13_14_manual_outcomes_exclude_no_outcomes.json"
    with open(json_file_rtf) as f:
        pseudo_anon_data_rtf = json.load(f)

    json_file_docx = "L:\\word_docs\\NLP\\5 manually_handled_keys_outcomes_edited_exclude_no_outcomes.json"
    with open(json_file_docx) as g:
        pseudo_anon_data_docx = json.load(g)
        


    # cycle through the POSITIVE/NEGATIVE files (terms present/absent) to find their keys via regex and then their outcomes

    No_surgery = 0
    Resection = 0
    Gold_ILAE_1 = 0
    Resection_No_Data = 0
    for file in positive_or_negative_files:
        with open(file) as f:
            pt_txt = f.read()
        

        pseudo_anon_docx = r"(?i)XXX pseudo_?anon_?dict_?DOCX (\d{1,4}) (?=XXX)"
        pseudo_anon_rtf = r"(?i)XXX pseudo_?anon_?dict_?RTF (\d{1,4}) (?=XXX)"
        
        if re.search(pseudo_anon_docx, pt_txt):
            uuid_no = re.search(pseudo_anon_docx, pt_txt)
            rtf_origin = False
        elif re.search(pseudo_anon_rtf, pt_txt):
            uuid_no = re.search(pseudo_anon_rtf, pt_txt)
            rtf_origin = True
        else:
            print("no pseudo anon uuid found!! major error in regex never seen this before.")
        
        uuid_no = uuid_no.group().split()[-1]
        
        if rtf_origin:
            outcom = pseudo_anon_data_rtf[str(uuid_no)]['MDT_Surgery_Outcome']
            MRN = pseudo_anon_data_rtf[str(uuid_no)]['MRN']
        elif not rtf_origin:
            outcom = pseudo_anon_data_docx[str(uuid_no)]['MDT_Surgery_Outcome']
            MRN = pseudo_anon_data_docx[str(uuid_no)]['MRN']
        
        
        
        
        outcomstr = str(outcom).replace(' ', '_') 
        if outcomstr == "No_surgery":
            
            No_surgery += 1
            
            # add to an already created separate No_surgery df before continuing
            if MRN not in list(df_No_surgery['MRN']):
                # add the MRN to this column:
                df_No_surgery = df_No_surgery.append({'MRN':MRN, semiology_key:add_1_or_0}, verify_integrity=True, ignore_index=True)
            
            elif MRN in list(df_No_surgery['MRN']): # MRN already in this df from a different file OR SEMIOLOGY CYCLE.
                # NEVER CHANGE A ONE TO ZERO BUT OPPOSITE IS OK - 
                    # If  CHANGED REGEX SEMIOLOGY YAML DICT - then reset the relevvant colulmn of df to Nans
                # CHANGE ONES TO ZERO ONLY ON NEGATION (LATER/MANUAL)
                # check value of semiology is 1 as positive files:
                if df_No_surgery.loc[df_No_surgery['MRN'] == MRN, semiology_key].item() == 1:
                    if add_1_or_0==0:
                        pass
                        # print("df_No_surgery duplicate MRN was in positive files from postitive_files_cycle. \
                        #     - this should not occur if terms_cycle was correct", file)
                    elif add_1_or_0==1:
                        pass
                        # print("df_No_surgery duplicate MRN already 1 from a previous file - this is ok")
                elif df_No_surgery.loc[df_No_surgery['MRN'] == MRN, semiology_key].item() == 0:
                    if add_1_or_0==0:
                        pass
                        # print("df_No_surgery value for semiology already 0 from prev file - this is ok")
                    elif add_1_or_0==1:
                        print("df_No_surgery value for semiology should be 1 but major error")
                        print("this should never happen if running positive files first then negative ones RECHECK")
                else:
                    # then must be a NaN entry:
                    df_No_surgery.loc[df_No_surgery['MRN'] == MRN, semiology_key] = add_1_or_0
            continue

            
            
            
            
        elif outcomstr == "Resection":
            Resection += 1
        elif outcomstr == "Gold_ILAE_1":
            Gold_ILAE_1 += 1
        elif outcomstr == "Resection_No_Data":
            Resection_No_Data += 1

        MRN_list = had_surgery_MRNs + gold_outcomes_list
        if MRN not in MRN_list:
            print("oops major inconsistency as these files had surgery but MRN was not found in list of MRNs who had surgery", MRN, file)

        
        # now find the row which contains the MRN and add a FALSE to the relevant semiology column:
        df.loc[df['MRN1'] == MRN, semiology_key] = add_1_or_0
        df.loc[df['MRN2'] == MRN, semiology_key] = add_1_or_0
        df.loc[df['MRN3'] == MRN, semiology_key] = add_1_or_0
        df.loc[df['MRN4'] == MRN, semiology_key] = add_1_or_0
        
    print("No surgery = ", No_surgery,
            "\nResection = ", Resection,
            "\nGold ILAE 1 = ", Gold_ILAE_1,
            "\nResection No Data = ", Resection_No_Data)

    return df, df_No_surgery