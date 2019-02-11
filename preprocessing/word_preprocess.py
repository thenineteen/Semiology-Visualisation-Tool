"""
Read word document texts for patients with
Epilepsy, read drugs table, remove sensitive data,
pseudo-anonymise and store new popped text
and original in separate folders.
Need to already have created new directory.

This contains all the functions called by main_docx_preprocess

Ali Alim-Marvasti (c) Jan 2019
"""
# below only works for docx
# so first convert .doc to .docx via .ps1
import docx
import os.path
import re
try:
    from xml.etree.cElementTree import XML
except ImportError:
    from xml.etree.ElementTree import XML
import zipfile
import io


def args_for_loop(*args):
    """
    factor function used by epilepsy_docx
    makes a list of two numbers
    """

    list = []
    for arg in args:
        list.append(arg)
    return list


def update_txt_docx(pt_txt, pt_docx_list, p, clean, print_p_by_p=False):
    """
    This function is a factor function called by epilepsy_docx.

    1. pt_txt and pt_docx_list are updated paragraph by paragraph.
    2. p is the paragraph contents from docx Document class.
    3. clean option strips the text
    4. print_p_by_p is an option to print out the text as it is being read.

    """

    pt_txt = pt_txt + '\n' + p.text
    pt_docx_list.append(p.text)

    if print_p_by_p:
        print(p.text)

    if clean:
        pt_txt = pt_txt.strip()

    return pt_txt, pt_docx_list


def save_as_txt(path_to_doc, pt_txt, save_path="L:\\word_docs\\texxts\\"):
    """
    save as text file in chosen already created directory
    """
    pt_txt = pt_txt.replace('\u03a8', 'Psych')
    pt_txt = pt_txt.replace('\u2192', '>')
    pt_txt = pt_txt.replace('\u03c8', '>')
    pt_txt = pt_txt.replace('\u25ba', '>')
    # otherwise gives charmap codec error

    save_filename = path_to_doc.split("\\")[-1].replace(
        '.docx', '.txt')  # takes name of docx file
    complete_filename = os.path.join(save_path, save_filename)
    with open(complete_filename, "w") as f:
        print(pt_txt, file=f)


def epilepsy_docx(path_to_doc, *paragraphs, read_tables=False, clean=False,
                  print_p_by_p=False):
    """
    Returns pt_txt as text.
    Returns pt_docx_list as list of paragraphs.
    Returns pt_meds_list as list of the table - needs further cleanup.
    can also print the text of .docx file.

    path_to_doc includes full folders and filename and extension.

    paragraphs: optional,
      reads between two paragraph numbers (inclusive).
      if not specified, or too many numbers specified, reads all paragraphs.
      if only one number specified, reads from paragraph 0
        to the number specified.

    read_tables will read the tables as paragraphs, if True.

    clean if default false will print(pt_txt) in same format as seen in jupyter
    if true will print(pt_txt) all new lines together with empty lines.
    I prefer clean=True

    print_p_by_p will print paragraph by paragraph as reading the docx file
    """

    document = docx.Document(path_to_doc)

    pt_txt = ''  # initialise text string
    pt_docx_list = []  # initialise patient's docx list
    pt_meds_list = []  # initialise patient meds list

    if paragraphs:
        para_list = args_for_loop(*paragraphs)

    if len(paragraphs) == 2:
        for n, p in enumerate(document.paragraphs):
            if n >= para_list[0] and n <= para_list[1]:
                pt_txt, pt_docx_list = update_txt_docx(pt_txt, pt_docx_list, p,
                                                       clean, print_p_by_p)

    elif len(paragraphs) == 1:
        for n, p in enumerate(document.paragraphs):
            if n >= 0 and n <= para_list[0]:
                pt_txt, pt_docx_list = update_txt_docx(pt_txt, pt_docx_list, p,
                                                       clean, print_p_by_p)

    else:
        for p in document.paragraphs:
            pt_txt, pt_docx_list = update_txt_docx(pt_txt, pt_docx_list, p,
                                                   clean, print_p_by_p)

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

    pt_docx_list = [i.lower() for i in pt_docx_list]
    pt_docx_list = [o for o in pt_docx_list if o != '' and
                    o != '\t' and o != ' ']

    pt_meds_list_clean_and_lower = [
        itm.lower() for itm in pt_meds_list if itm != '' and itm != '\t']
    pt_meds_list_clean_phenytoin = [
        s.replace('  ', '') for s in pt_meds_list_clean_and_lower]
    pt_meds_list_clean_phenytoin = [med.replace(
        'phenytoin ', 'phenytoin') for med in pt_meds_list_clean_phenytoin]
    pt_meds_list = pt_meds_list_clean_phenytoin  # simpler rename

    # save_as_txt(path_to_doc, pt_txt)

    return pt_txt, pt_docx_list, pt_meds_list


def epilepsy_docx_xml(path):
    """
    Take the path of a docx file as argument, return the text in unicode.
    Run this if epilepsy_docx() isn't able to read the name.
    This should automatically read tables anyway.
    """

    WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    PARA = WORD_NAMESPACE + 'p'
    TEXT = WORD_NAMESPACE + 't'

    document = zipfile.ZipFile(path)
    xml_content = document.read('word/document.xml')
    document.close()
    tree = XML(xml_content)

    paragraphs = []
    for paragraph in tree.getiterator(PARA):
        texts = [n.text for n in paragraph.getiterator(TEXT) if n.text]
        if texts:
            paragraphs.append(''.join(texts))

    pt_txt_xml = '\n\n'.join(paragraphs)
    # save_as_txt(path, pt_txt_xml)

    return pt_txt_xml


def anonymise_name_txt(pt_txt, silent=False, xml=False):
    """
    finds first and surnames using regex and replaces them with
    redact messages XXXfirstnameXXX and XXXsurnameXXX respectively.

    If you want instead of the default redact message
    to have a single space, use silent=True.

    xml option's regex is required when text was read by epilepsy_docx_xml.
    """

    if silent:
        redact_message_fname = ' '
        redact_message_sname = ' '
    else:
        redact_message_fname = 'XXXfirstnameXXX'
        redact_message_sname = 'XXXsurnameXXX'

    if xml:
        name_pattern = r"Name[\s\t:]?\w+[\s+]\w+"
        name_search = re.search(name_pattern, pt_txt)
        name = name_search.group()
        name = name.split()
        firstname = name[0]
        surname = name[1]

    else:
        try:
            name_pattern = r"Name[\s\t:]+\w+[\s+]\w+"
            name_search = re.search(name_pattern, pt_txt)
            name = name_search.group()
            name_list = name.split()
            firstname = name_list[1]
            surname = name_list[2]
        except IndexError:
            name = name.replace('Name:', '')
            name_list = name.split()
            firstname = name_list[0]
            surname = name_list[1]

    pt_txt_fnamefilter = pt_txt.replace(firstname, redact_message_fname)
    pt_txt_sfnamefilter = pt_txt_fnamefilter.replace(
        surname, redact_message_sname)

    return pt_txt_sfnamefilter


def anonymise_DOB_txt(pt_txt, redact_message='XXX-DOB-XXX', xml=False):
    """
    finds DOB using regex and replaces with
    redact message 'XXX-DOB-XXX'.

    If you want instead of the default redact message
    to have anything else, specify.

    If you want the pseudo-anonymised Pt ID to be there instead, use
    redact_message = "IDP"

    xml option's regex is required when text was read by epilepsy_docx_xml.
    """

    if xml:
        try:  # DD/MM/YY(YY) or DD.MM.YY(YY) or DD - MM - YY(YY)
            DOB_pattern = r"DOB[\s\t:]+[0-9]+\s?/?\.?-?\s?[0-9]+\s?/?\.?-?\s?[0-9]+"
            DOB_match = re.search(DOB_pattern, pt_txt)
            DOB = DOB_match.group()

        except AttributeError:  # DD FEB YY(YY) or DD-Feb-YY or . or / or combinations
            DOB_pattern = r"DOB[\s\t:]+[0-9]+\s?/?\.?-?\s?[0-9]*\w*\s?/?\.?-?\s?[0-9]+"
            DOB_match = re.search(DOB_pattern, txt)
            DOB = DOB_match.group()

    else:  # currently same as above
        try:  # DD/MM/YY(YY) or DD.MM.YY(YY) or DD - MM - YY(YY)
            DOB_pattern = r"DOB[\s\t:]+[0-9]+\s?/?\.?-?\s?[0-9]+\s?/?\.?-?\s?[0-9]+"
            DOB_match = re.search(DOB_pattern, pt_txt)
            DOB = DOB_match.group()

        # DD FEB YY(YY) or DD-Feb-YY or . or / or combinations
        except AttributeError:
            DOB_pattern = r"DOB[\s\t:]+[0-9]+\s?/?\.?-?\s?[0-9]*\w*\s?/?\.?-?\s?[0-9]+"
            DOB_match = re.search(DOB_pattern, txt)
            DOB = DOB_match.group()

    pt_txt_DOBfilter = pt_txt.replace(DOB, redact_message)

    return pt_txt_DOBfilter
