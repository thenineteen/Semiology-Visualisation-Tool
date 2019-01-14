
"""
Read word document texts for patients with
Epilepsy, remove sensitive data,
pseudo-anonymise and store new popped text
and original in separate folders
Ali Alim-Marvasti (c) Jan 2019
"""
# below only works for docx
# so first convert .doc to .docx
import docx

path_to_doc = "L:\\word docs\\Brady, Gary.docx"
document = docx.Document(path_to_doc)
# document.save('L:\\word docs\\testing.docx')


def args_for_loop(*args):
    list = []
    for arg in args:
        list.append(arg)
    return list


def epilepsy_docx_document(path_to_doc, *paragraphs):
    """
    prints the text of .docx file. 
    paragraphs: optional,
      reads between two paragraph numbers (inclusive).
      if not specified, or too many numbers specified, reads all paragraphs.
      if only one number specified, reads from paragraph 0
        to the number specified. 
    """
    document = docx.Document(path_to_doc)

    if paragraphs:
        para_list = args_for_loop(*paragraphs)

    if len(paragraphs) == 2:
        for n, p in enumerate(document.paragraphs):
            if n >= para_list[0] and n <= para_list[1]:
                print(p.text)

    elif len(paragraphs) == 1:
        for n, p in enumerate(document.paragraphs):
            if n >= 0 and n <= para_list[0]:
                print(p.text)

    else:
        for p in document.paragraphs:
            print(p.text)
    return
