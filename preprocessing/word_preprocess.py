"""
Read word document texts for patients with
Epilepsy, read drugs table, remove sensitive data,
pseudo-anonymise and store new popped text
and original in separate folders

Ali Alim-Marvasti (c) Jan 2019
"""
# below only works for docx
# so first convert .doc to .docx via .ps1
import docx
import os.path
import re


def args_for_loop(*args):
    list = []
    for arg in args:
        list.append(arg)
    return list


def update_txt_docx(pt_txt, pt_docx, p, clean):
    pt_txt = pt_txt + p.text
    pt_docx.append(p.text)
    print(p.text)

    if clean:
        pt_txt = pt_txt.strip()

    return pt_txt, pt_docx


def epilepsy_docx(path_to_doc, *paragraphs, read_tables=False, clean=False):
    """
    prints the text of .docx file. 
    paragraphs: optional,
      reads between two paragraph numbers (inclusive).
      if not specified, or too many numbers specified, reads all paragraphs.
      if only one number specified, reads from paragraph 0
        to the number specified.
    read_tables will read the tables as paragraphs, if True.
    Returns pt_docx as list of paragraphs.
    Returns pt_meds_list as list of the table - needs further cleanup.
    """
    document = docx.Document(path_to_doc)

    pt_txt = ''  # initialise text string
    pt_docx = []  # initialise patient's docx list
    pt_meds_list = []  # initialise patient meds list

    if paragraphs:
        para_list = args_for_loop(*paragraphs)

    if len(paragraphs) == 2:
        for n, p in enumerate(document.paragraphs):
            if n >= para_list[0] and n <= para_list[1]:
                pt_txt, pt_docx = update_txt_docx(pt_txt, pt_docx, p, clean)

    elif len(paragraphs) == 1:
        for n, p in enumerate(document.paragraphs):
            if n >= 0 and n <= para_list[0]:
                pt_txt, pt_docx = update_txt_docx(pt_txt, pt_docx, p, clean)

    else:
        for p in document.paragraphs:
            pt_txt, pt_docx = update_txt_docx(pt_txt, pt_docx, p, clean)

    if read_tables:
        for t in document.tables:
            for row in t.rows:
                for cell in row.cells:
                    for paragraph in cell.paragraphs:
                        pt_meds_list.append(paragraph.text)
                        # print(paragraph.text)
        # print (pt_meds_list)

    # this next part cleans to remove empty characters and spaces
    if clean:
        pt_txt = pt_txt.replace('\t', ' ')
        pt_txt = pt_txt.strip()

    pt_docx = [i.lower() for i in pt_docx]
    pt_docx = [o for o in pt_docx if o != '' and o != '\t' and o != ' ']

    pt_meds_list_clean_and_lower = [
        itm.lower() for itm in pt_meds_list if itm != '' and itm != '\t']
    pt_meds_list_clean_phenytoin = [
        s.replace('  ', '') for s in pt_meds_list_clean_and_lower]
    pt_meds_list_clean_phenytoin = [med.replace(
        'phenytoin ', 'phenytoin') for med in pt_meds_list_clean_phenytoin]
    pt_meds_list = pt_meds_list_clean_phenytoin  # simpler rename

    # saves as txt
    save_path = "L:\\word_docs\\texxts\\"
    save_filename = path_to_doc.split("\\")[3].replace(
        '.docx', '')+".txt"  # takes name of docx file
    complete_filename = os.path.join(save_path, save_filename)
    with open(complete_filename, "w") as f:
        f.write(pt_txt)

    return pt_txt, pt_docx, pt_meds_list


def anonymise_txt(pt_txt, silent=False, clean=False):
    """
    finds first and surnames using regex and replaces them with
    redact messages XXXfirstnameXXX and XXXsurnameXXX respectively.

    If you want instead of the default redact message
    to have a single space, use silent=True.
    """
    if silent:
        redact_message_fname = ' '
        redact_message_sname = ' '
    else:
        redact_message_fname = 'XXXfirstnameXXX'
        redact_message_sname = 'XXXsurnameXXX'

    if clean:
        pt_txt = pt_txt.replace('\n', ' ')
        pt_txt = pt_txt.replace('\t', ' ')

    name_pattern = r"Name[\s:]+\w+[\s+]\w+"
    name_search = re.search(name_pattern, pt_txt)
    name = name_search.group()
    name = name.split()
    firstname = name[1]
    surname = name[2]

    pt_txt_fnamefilter = pt_txt.replace(firstname, redact_message_fname)
    pt_txt_sfnamefilter = pt_txt_fnamefilter.replace(
        surname, redact_message_sname)

    return pt_txt_sfnamefilter
