import os
import numpy as np
import pandas as pd

import nltk
from nltk.corpus import treebank
from nltk.corpus import stopwords
from collections import Counter

import string


def open_txt_file(path_to_doc):
    with open(path_to_doc) as f:
        pt_txt = f.read()

    return pt_txt


def save_filtered_txt_file(path_to_doc, filtered_pt_txt_tokens, save_path):
    try:
        save_filename = path_to_doc.split("\\")[-1]
        complete_filename = os.path.join(save_path, save_filename)
        with open(complete_filename, "w") as f:
            f.write(filtered_pt_txt_tokens)

        print("{} success".format(save_filename))
    
    except:
        print("FAILED: {}".format(save_filename))
        raise


def filter_and_tokenise(pt_txt, nltk_stopword=True):
    tokens = nltk.word_tokenize(pt_txt) #  tokenss

    if nltk_stopword:
        # remove all nltk stopwords
        filtered_pt_txt_tokens = str([word for word in tokens if word.lower() not in stopwords.words('english')])
            # changed to list
            # stopwords are all lowercase words
        
        # remove all punctuation
        filtered_pt_txt_tokens = filtered_pt_txt_tokens.translate(str.maketrans('', '', string.punctuation))

        # # change back to tokens
        # filtered_pt_txt_tokens = nltk.word_tokenize(filtered_pt_txt_tokens)


        return filtered_pt_txt_tokens
    
    else:
        return tokens





def main_filter_tokenise_Pos_NER(path_to_folder="L:\\word_docs\\pytest\\empty",
                                 nltk_stopword=True,
                                 save_path_tokenised="L:\\word_docs\\NLP\\filtered_tokenised\\",
                                 save_path_posNER_tagged="L:\\word_docs\\NLP\\Pos_NER_tagged\\",
                                 Perform_Pos_NER=False,
                                 count_tokens=False):

    """
    This saves a string of the pt_txt without stopwords or punctuation if the nltk_stopword option is used.
    Returns a list of tokens.
    The POS tagging does not work - things all are NNP whether we use the stopword option or not.
    Maybe need sklearn's toolbox?
    """

    for txt_file in os.listdir(path_to_folder):
        path_to_doc = os.path.join(path_to_folder, txt_file)
        
        #open the file and filter/tokenise
        pt_txt = open_txt_file(path_to_doc)
        filtered_pt_txt_tokens = filter_and_tokenise(pt_txt, nltk_stopword)

        #save tokenise result
        save_filtered_txt_file(path_to_doc, str(filtered_pt_txt_tokens), save_path_tokenised)

        #pos tagging and NER ready for lemmatisation if required and save as string to txt file
        if Perform_Pos_NER:
            # pos tag the tokens without the stopwords/punctuation removal
            # (otherwise all are NNP)
            pt_txt_tokens_nostopwords = filter_and_tokenise(pt_txt, nltk_stopword)
            tagged_pt_txt = nltk.pos_tag(pt_txt_tokens_nostopwords)
            save_filtered_txt_file(path_to_doc, str(tagged_pt_txt), save_path_posNER_tagged)

        if count_tokens:
        # change back to tokens   
            filtered_pt_txt_tokens = nltk.word_tokenize(filtered_pt_txt_tokens)
            count = Counter(filtered_pt_txt_tokens)
            print (count.most_common(10))

    last_file_filtered_pt_txt_tokens = filtered_pt_txt_tokens
    return last_file_filtered_pt_txt_tokens