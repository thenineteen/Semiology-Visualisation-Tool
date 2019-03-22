import yaml
import re
from NLP.term_phrase_outcome import *

# load the fixtyres.yaml file: yaml_file
pass

# cycle through the revelant terms (lists in yaml file)
for semiology in yaml_file['semiology']['temporal']:
    term_or_precise_phrase = re.compile(semiology)

    term_phrase_outcome(
        *term_or_precise_phrase, # ensure term exists in the files e.g. don't use a full word on stemmed texts
        path_to_folder,  # files to look in for the term
        outcomes_json_file_specified=False,
        stemmed=False)  # use original files - ensure folder above matches and is not a stemmed version of the files


        

