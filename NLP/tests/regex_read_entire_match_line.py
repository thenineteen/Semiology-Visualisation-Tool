import re
import os
try:
    from NLP.term_phrase_outcome import *
except:
    from .term_phrase_outcome import *

def regex_read_entire_match_line(
    regex_pattern,
    single_large_combined_txt_file="L:\\word_docs\\NLP\\all_folder_replaced_quotes\\all_txt_in_single_file_not_stemmed.txt"):
    """
    When coming up with the semiology dictionary, use the semiology_terms here to scout the appropriate NLA/NLB regex uses.
    Use a .txt file which has all the other texts appended.

    findall_list is list of all match terms from findall - inspect for false positives.

    IGNORES CASE 
    """

    single_large_combined_txt_file = os.path.join(single_large_combined_txt_file,)

    with open(single_large_combined_txt_file) as f:
        txt = f.read()
 
    regex_pattern = "(?i)" + regex_pattern 
    regex_pattern = re.compile(regex_pattern)
    findall = re.findall(regex_pattern, txt)
    findall_list = list(findall)



    return findall_list

