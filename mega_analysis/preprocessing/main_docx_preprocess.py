
import os
import json
import re

try:
    from word_preprocess import args_for_loop, update_txt_docx, save_as_txt
    from word_preprocess import epilepsy_docx_to_txt, epilepsy_docx_xml_to_txt 
    from word_preprocess import name_pattern_regex, pt_txt_replace
    from word_preprocess import anonymise_name_txt, anonymise_DOB_txt, anon_hosp_no
except:
    from .word_preprocess import args_for_loop, update_txt_docx, save_as_txt
    from .word_preprocess import epilepsy_docx_to_txt, epilepsy_docx_xml_to_txt 
    from .word_preprocess import name_pattern_regex, pt_txt_replace
    from .word_preprocess import anonymise_name_txt, anonymise_DOB_txt, anon_hosp_no


def main_docx_preprocess(path_to_folder, *paragraphs, read_tables=False,
                         clean=False, save_path_anon="L:\\word_docs\\texxts\\",
                         json_dictionary_file = 'L:\\word_docs\\keys.json', DOCX=True,
                         docx_to_txt_save_path="L:\\word_docs\\epilepsy_docx_to_txt\\",
                         docx_xml_to_txt_save_path="L:\\word_docs\\epilepsy_docx_xml_to_txt\\",
                         Suppress_messages=False):
    """
    This runs the functions from word_preprocess.py in an entire folder.

    run using these two lines like this:
    path_to_folder = 'L:\\word_docs\\test\\'
    main_docx_preprocess(path_to_folder, read_tables=False, clean=False, json_dictionary_file = , save_path="L:\\word_docs\\texxts\\")

    Runs epilepsy_docx_to_txt converter first. 
    If this fails to obtain name or DOB, runs epilepsy_docx_xml_to_txt.
    If both fail, gives error message wrt name or DOB. (MRN doesn't use xml)

    (The format of the output of epilepsy_docx_to_txt is better than xml's -
    But xml can read the medication tables and some DOB which the other can't).

    >json_dictionary_file determines where to save the keys:values of sensitive data.

    >DOCX False is option when converting files that are already in .txt format
    i.e. skip the docx to txt conversion e.g. for RTF files. revert to RTF branch for working condition.

    >Suppress_messages: if True, will only print important messages. 

    >docx_to_txt_save_path and docx_xml_to_txt_save_path are intermediate folder paths to store outcome of related function on .docx 
    i.e. before anonymisation

    *paragraphs is redundant - can specify which paragraph numbers to read from.
    initially was useful in obtaining structure for regex.

    main_docx_preprocess stores sensitive data as dictionary in .json file.
    (MRN is the actual hospital number innerkey)
    i.e.:
    psuedo_anon_dict: {"MRN": MRN, "Names": [names], "DOB": DOB_actual}


    keys are stored in:
    'L:\\word_docs\\word_keys2.json' for DOCX
    L:\\word_docs\\word_RTF_keys.json for TXT

    Afterwards, run the gold_outcomes_MRNs() function in outcomes.py to get list of labels
    and add the labels to the above keys using the find_MRN_label_outcomes() function in json_keys_read.py.

    Ali Alim-Marvasti (c) Jan-Feb 2019
    """

    pseudo_anon_dict = {}  # uuid pseudononymisation to hosp no (mrn)
    MRN_dict = {}  # hosp no to names

    if DOCX:  # read and convert docx to .txt then work on it
        n_docx = 0
        n_xml = 0
        n_docx_name_anon = 0
        n_docx_p_name_anonxml = 0  # using xml = true for first few paragraphs
        n_xml_name_anon = 0
        n_DOB_anon = 0
        n_DOB_anon_xml = 0  # same DOB function but xml to read DOB first
        uuid_no = 0  # pseudononymised replacement for MRN
        n_uuid = 0  # number MRNs found and replaced
        n_uuid_name_of_doc = 0  # MRNs extracted from document name

        for docx_file in os.listdir(path_to_folder):
            name_error_message = False
            DOB_error_message = False
            mrn_error_message = False

            path_to_doc = os.path.join(path_to_folder, docx_file)

            pt_txt, pt_docx_list, pt_meds_dict = epilepsy_docx_to_txt(
                path_to_doc, *paragraphs, read_tables=False, clean=False,
                docx_to_txt_save_path=docx_to_txt_save_path)

            n_docx += 1
            uuid_no += 1

            # now anonymise names first
            try:  # sometimes there is no actual name after "Name:" in the file
                pt_txt, names = anonymise_name_txt(pt_txt, path_to_doc)
                n_docx_name_anon += 1

            except AttributeError:
                # before running other xml reader:
                try:
                    # read first few paragraphs only:
                    pt_txt_beginning, pt_docx_list, pt_meds_dict = epilepsy_docx_to_txt(
                        path_to_doc, 0,5, read_tables=False, clean=False, docx_to_txt_save_path=docx_to_txt_save_path)

                    if re.search(r"telemetry\s*report", pt_txt_beginning.lower()):
                        print('VT/Neurophys report?: {}\nThis file was skipped.'.format(docx_file))
                        # take back the counters
                        n_docx -= 1
                        uuid_no -= 1  
                        continue  # continue with next file

                    else:
                        # try to find name in first few paragraphs:
                        pt_txt_beginning_anon, names = anonymise_name_txt(pt_txt_beginning, path_to_doc, xml=True)

                        # use [names] to redact names in the original pt_txt which didn't use paragraphs option
                        pt_txt_sfnamefilter, names = pt_txt_replace (names[0], names[1], pt_txt)
                        pt_txt = pt_txt_sfnamefilter
                        n_docx_p_name_anonxml += 1

                        if not Suppress_messages:
                            print('\nUsed anonymise_name xml=true for 5 paragraphs without docx_xml for {}'.format(docx_file))

                except AttributeError:
                    # if no name found, run the other docx XML function
                    try:
                        pt_txt, n_xml = epilepsy_docx_xml_to_txt(path_to_doc, n_xml, docx_xml_to_txt_save_path=docx_xml_to_txt_save_path)
                        pt_txt, names = anonymise_name_txt(pt_txt, path_to_doc, xml=True)
                        n_xml_name_anon += 1

                    except:  # admit anon_name defeat
                        name_error_message = True
                        # only prints name_error if both above under try: clause fail
                        names = ['No Name', 'No Name']

            except:  # so it doesn't stop iterating for loop
                print("major uncaught exception: anonymise_name_txt failed even before xml try, for \t\t{}\n ".format(
                    docx_file))
                name_error_message = True
                names = ['No Name', 'No Name']



            


            # whether it did anonymise name or not,
            # anonymise hosp no
            # anon_DOB
            # save the name and hosp no txt

            # anonymise hosp number
            pt_txt, MRN, n_uuid, n_uuid_name_of_doc, mrn_error_message =\
                anon_hosp_no(pt_txt, path_to_doc, uuid_no, n_uuid, n_uuid_name_of_doc)

            # now anonymise DOB
            try:
                pt_txt, n_DOB_anon, DOB_actual = anonymise_DOB_txt(pt_txt, n_DOB_anon)

            except:
                # if no DOB found, run the other docx XML function
                try:
                    pt_txt_xml, n_xml = epilepsy_docx_xml_to_txt(
                        path_to_doc, n_xml, docx_xml_to_txt_save_path=docx_xml_to_txt_save_path)
                    DOB_anon_message, n_DOB_anon_xml, DOB_actual = anonymise_DOB_txt(
                        pt_txt_xml, n_DOB_anon_xml, xml=True)
                    pt_txt = pt_txt.replace(DOB_actual, DOB_anon_message)

                except AttributeError:
                    DOB_error_message = True
                    DOB_actual = "XX/XX/XX"
                except ValueError:
                    DOB_error_message = True
                    DOB_actual = "XX/XX/XX"
                except TypeError:
                    DOB_error_message = True
                    DOB_actual = "XX/XX/XX"

            # save the .txt file with names/DOB/MRN redacted
            # save (with meds list appended: change to pt_txt + str(pt_meds_dict))
            save_as_txt(path_to_doc, pt_txt, save_path_anon)

            # store the dictionary of keys for this patient
            pseudo_anon_dict[uuid_no] = {"MRN": MRN, "Name": names, "DOB": DOB_actual}
            if not Suppress_messages:
                if name_error_message or DOB_error_message or mrn_error_message:
                    print("\n{}".format(docx_file))
                if name_error_message:
                    print("*anonymise_name and xml=true failed for above.")
                    print("May not have \"Name\" field or this may not be a presurgical MDT file")
                if DOB_error_message:
                    print("**DOB not found for \t\t{}".format(docx_file))
            if mrn_error_message:
                print("***MRN pattern not found for \t\t{}\n".format(path_to_doc))

            # end of loop over all docx files



        # store keys of all MRNs, names and DOB
        # write all keys to json dictionary file
        try:
            with open(json_dictionary_file, 'w') as file:

                file.seek(0)  # rewind

                json.dump(pseudo_anon_dict, file)
                #file.write(json.dumps(pseudo_anon_dict))

                file.truncate()

        except TypeError:
            print("dict keys not string for {}".format(docx_file))



        print('\n\n# epilepsy_docx_to_txt() = \t\t\t{}'.format(n_docx))
        print('\tof which anonymise_name_txt() = \t{}'.format(n_docx_name_anon))
        print('\t anon_name_xml=True on 5 paragraphs = \t{}'.format(n_docx_p_name_anonxml))
        print('\tof which #anonymise_DOB() = \t\t{}\n'.format(n_DOB_anon))
        print('# epilepsy_docx_xml_to_txt = \t\t\t{}'.format(n_xml))
        print('\tof which anonymise_name_txt(xml) = \t{}'.format(n_xml_name_anon))
        print('\tof which anonymise_DOB(xml) = \t\t{}\n'.format(n_DOB_anon_xml))
        print('# of hosp_no MRNs found and replaced = \t\t{}/{}'.format(n_uuid, uuid_no))
        print('# of MRNs extracted from document name = \t{}/{}'.format(n_uuid_name_of_doc, uuid_no))


# doesn't really work - revert to the RTF branch
    else:  # only read the .txt files from folder given
        n_txt = 0
        #n_xml = 0
        n_TXT_name_anon = 0
        #n_xml_name_anon = 0
        n_DOB_anon = 0
        n_DOB_anon_xml = 0  # same DOB function but xml to read DOB first
        uuid_no = 0  # pseudononymised replacement for MRN
        n_uuid = 0  # number MRNs found and replaced
        n_uuid_name_of_doc = 0  # MRNs extracted from document name

        for TXT_file in os.listdir(path_to_folder):
            path_to_doc = os.path.join(path_to_folder, TXT_file)

            name_error_message = False
            DOB_error_message = False
            mrn_error_message = False

            with open(path_to_doc, "r", errors='backslashreplace') as f:
                pt_txt = f.read()
                
                n_txt += 1
                uuid_no += 1

                # now anonymise names
                try:  # sometimes there is no actual name after "Name:" in the file
                    pt_txt, names = anonymise_name_txt(pt_txt, path_to_doc)
                    n_TXT_name_anon += 1




                except AttributeError:
                    # before running other xml reader:
                    try:
                        # read first few paragraphs only:
                        pt_txt_beginning = f.read(5)

                        if re.search(r"telemetry\s*report", pt_txt_beginning.lower()):
                            print('VT/Neurophys report?: {}\nThis file was skipped.'.format(docx_file))
                            # take back the counters
                            n_docx -= 1
                            uuid_no -= 1  
                            continue  # continue with next file

                        else:
                            # try to find name in first few paragraphs:
                            pt_txt_beginning_anon, names = anonymise_name_txt(pt_txt_beginning, path_to_doc, xml=True)

                            # use [names] to redact names in the original pt_txt which didn't use paragraphs option
                            pt_txt_sfnamefilter, names = pt_txt_replace (names[0], names[1], pt_txt)
                            pt_txt = pt_txt_sfnamefilter
                            n_docx_p_name_anonxml += 1

                            print('\nUsed anonymise_name xml=true for 5 lines without docx_xml for {}'.format(docx_file))

                    except AttributeError:
                        # if no name found, run the other docx XML function
                        try:
                            
                            pt_txt, names = anonymise_name_txt(pt_txt, path_to_doc, xml=True)
                            n_xml_name_anon += 1

                        except:  # admit anon_name defeat
                            name_error_message = True
                            # only prints name_error if both above under try: clause fail
                            names = ['No Name', 'No Name']

                except:  # so it doesn't stop iterating for loop
                    print("major uncaught exception: anonymise_name_txt failed even before xml try, for \t\t{}\n ".format(
                        docx_file))
                    name_error_message = True
                    names = ['No Name', 'No Name']







                # whether it did anonymise name or not,
                # anonymise hosp no
                # anon_DOB
                # save the name and hosp no txt

                # anonymise hosp number
                pt_txt, MRN, n_uuid, n_uuid_name_of_doc, mrn_error_message =\
                    anon_hosp_no(pt_txt, path_to_doc, uuid_no,
                                n_uuid, n_uuid_name_of_doc)

                # now anonymise DOB
                try:
                    pt_txt, n_DOB_anon, DOB_actual = anonymise_DOB_txt(pt_txt, n_DOB_anon)

                except:
                    # if no DOB found, run with xml option = True
                    try:
                        DOB_anon_message, n_DOB_anon_xml, DOB_actual = anonymise_DOB_txt(
                            pt_txt, n_DOB_anon_xml, xml=True)
                        pt_txt = pt_txt.replace("DOB", DOB_anon_message)

                    except AttributeError:
                        DOB_error_message = True
                        DOB_actual = "XX/XX/XX"

                    except IndexError:
                        DOB_error_message = True
                        print ('DOB[0,1,2] indexError for {}'.format(TXT_file))
                        DOB_actual = "XX/XX/XX"

                # save the .txt file with names/DOB/MRN redacted
                save_as_txt(path_to_doc, pt_txt, save_path_anon)

                # store the dictionary of keys for this patient
                pseudo_anon_dict[uuid_no] = {"MRN": MRN, "Name": names, "DOB": DOB_actual}

                if name_error_message or DOB_error_message or mrn_error_message:
                    print("\n{}".format(TXT_file))
                if name_error_message:
                    print("*anonymise_name failed for above.")
                    print("May not have \"Name\" field or this may not be a presurgical MDT file")
                if DOB_error_message:
                    print("**DOB not found for \t\t{}".format(TXT_file))
                if mrn_error_message:
                    print("***MRN pattern not found for \t\t{}\n".format(path_to_doc))

                # end of loop over all docx files

        # store keys of all MRNs, names and DOB
        # write all keys to json dictionary file
        try:
            with open(json_dictionary_file, 'w') as file:

                file.seek(0)  # rewind

                json.dump(pseudo_anon_dict, file)
                #file.write(json.dumps(pseudo_anon_dict))

                file.truncate()

        except TypeError:
            print("dict keys not string for {}".format(docx_file))

        print('\n\n# epilepsy_docx_to_txt() = \t\t\t{}'.format(n_txt))
        print('\tof which anonymise_name_txt() = \t{}'.format(n_TXT_name_anon))
        print('\tof which #anonymise_DOB() = \t\t{}'.format(n_DOB_anon))
        print('\tof which anonymise_DOB(xml) = \t\t{}'.format(n_DOB_anon_xml))
        print('# of hosp_no MRNs found and replaced = \t\t{}/{}'.format(n_uuid, uuid_no))
        print('# of MRNs extracted from document name = \t{}/{}'.format(n_uuid_name_of_doc, uuid_no))
