from preprocessing.word_preprocess import epilepsy_docx, epilepsy_docx_xml
from preprocessing.word_preprocess import anonymise_name_txt, save_as_txt
from preprocessing.word_preprocess import anonymise_DOB_txt
import os


def main_docx_preprocess(path_to_folder, *paragraphs, read_tables=False,
                         clean=False, save_path="L:\\word_docs\\test_anon_name_mrn\\", DOCX=True):
    """
    This runs the functions from word_preprocess.py in an entire folder. 

    run like this:
    path_to_folder = 'L:\\word_docs\\test_anonymise\\'
    
    main_docx_preprocess(path_to_folder, read_tables=True, clean=False)
    
    Runs docx first. if this fails, runs epilepsy_docx_xml.
    If both fail, gives error message. 
    
    TXT is when converting files that are already in .txt format
    Originally from the RTF files but then also can be sued for any even docx's which
    have been converted to .txt to avoid using original docx.
    """

    pseudo_anon_dict = {}  # uuid pseudononymisation to hosp no (mrn)
    MRN_dict = {}  # hosp no to names

    if DOCX:  # read and convert docx to .txt then work on it
        n_docx = 0
        n_xml = 0
        n_docx_name_anon = 0
        n_xml_name_anon = 0
        n_DOB_anon = 0
        n_xml_DOB_anon = 0
        uuid_no = 0  # pseudononymised replacement for MRN
        n_uuid = 0  # number MRNs found and replaced

        for docx_file in os.listdir(path_to_folder):
            path_to_doc = os.path.join(path_to_folder, docx_file)

            pt_txt, pt_docx_list, pt_meds_dict = epilepsy_docx_to_txt(
                path_to_doc, *paragraphs, read_tables=True, clean=False)

            n_docx += 1
            uuid_no += 1

            # now anonymise names first
            try:  # sometimes there is no actual name after "Name:" in the file
                pt_txt, names = anonymise_name_txt(pt_txt, path_to_doc)
                n_docx_name_anon += 1

            except AttributeError:
                 # if no name found, run the other docx XML function

                try:
                    pt_txt = epilepsy_docx_xml_to_txt(path_to_doc)
                    n_xml += 1
                    pt_txt, names = anonymise_name_txt(
                        pt_txt, path_to_doc, xml=True)
                    n_xml_name_anon += 1
                except:
                    print("anonymise_name and xml=true failed for {}.".format(
                        path_to_doc))
                    print(
                        "May not have \"Name\" field or this may not be a presurgical MDT file\n")
                    names = ['No Name', 'No Name']
                    continue

            except:
                print("major uncaught exception: anonymise_name_txt failed even before xml try, for {}\n ".format(
                    path_to_doc))
                names = ['No Name', 'No Name']
                continue

            # whether it did anonymise name or not,
                # hosp no anonymise uuid
                # save the name and hosp anon txt
            pt_txt, MRN, n_uuid = anon_hosp_no(
                pt_txt, path_to_doc, uuid_no, n_uuid)
            save_as_txt(path_to_doc, pt_txt + str(pt_meds_dict), save_path)
            MRN_dict[MRN] = names
            pseudo_anon_dict[uuid_no] = MRN_dict[MRN]

        try:
            with open('L:\\word_docs\\word_keys.json', 'w') as file:

                file.seek(0)  # rewind

                json.dump(pseudo_anon_dict, file)
                #file.write(json.dumps(pseudo_anon_dict))

                file.truncate()

        except TypeError:
            print("dict keys not string for {}".format(docx_file))

        # write all keys to json dictionary file

#         with open('L:\\word_docs\\word_keys.json', 'w') as file:
#             #json.dump(pseudo_anon_dict, file)
#             file.write(json.dumps(pseudo_anon_dict))

        print('# epilepsy_docx_to_txt() = \t\t\t{}'.format(n_docx))
        print('of which anonymise_name_txt() = \t\t{}'.format(n_docx_name_anon))
        print('of which #anonymise_DOB() = \t\t\t{}'.format(n_DOB_anon))
        print('# epilepsy_docx_xml_to_txt = \t\t\t{}'.format(n_xml))
        print('of which anonymise_name_txt(xml) = \t\t{}'.format(n_xml_name_anon))
        print('of which anonymise_DOB() = \t\t\t{}'.format(n_xml_DOB_anon))
        print('# of hosp_no MRNs found and replaced = \t\t{}/{}'.format(n_uuid, uuid_no))

    else:  # only read the txt files from folder given
        for RTF_file in os.listdir(path_to_folder):
            path_to_doc = os.path.join(path_to_folder, RTF_file)
            with open(path_to_doc) as f:
                pt_txt = f.read()

        #do above again
