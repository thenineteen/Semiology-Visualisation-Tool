# stem all the tokens returned from b_1_filter_and_tokenise.

from nltk.stem import *
from nltk.stem.porter import *
from nltk.stem.snowball import SnowballStemmer

try:
    from NLP.b_1_filter_and_tokenise import *
except:
    from .b_1_filter_and_tokenise import *

stemmer = SnowballStemmer("english")


def stem_all_txts(path_to_folder="L:\\word_docs\\NLP\\filtered_tokenised\\test\\",
                  save_path_stemmed="L:\\word_docs\\NLP\\stemming\\",
                  nltk_stopword=False, # False as already done change to true if not with filter and tokenise
                  future_option=False):


    for txt_file in os.listdir(path_to_folder):
        path_to_doc = os.path.join(path_to_folder, txt_file)
        
        #initialise
        stemmed_pt_txt = ""

        #open the file
        pt_txt = open_txt_file(path_to_doc)

        # need to toeknise the text again otherwise looking at individual characters
        tokenised_txt = filter_and_tokenise(pt_txt, nltk_stopword) # False as already done

        if nltk_stopword:
            for word in tokenised_txt:
                stemmed_pt_txt = stemmed_pt_txt + stemmer.stem(word) #?.lower()
        
        else:
            for word in tokenised_txt:
                stemmed_pt_txt = stemmed_pt_txt + " " + stemmer.stem(word) #?.lower()
        
        # save the stemmed_pt_txt
        save_filtered_txt_file(path_to_doc, stemmed_pt_txt, save_path_stemmed)



def count_tokens(txt_to_tokenise_and_count):
    """
    stores all counts, prints top 10. 
    """

    txt_tokens = nltk.word_tokenize(txt_to_tokenise_and_count)    
    counts = Counter(txt_tokens)

    print (counts.most_common(10))
    return counts


def amalgamate_all_txts_into_one(
    path_to_folder="L:\\word_docs\\NLP\\stemming\\combinedRTFDOCX\\",
    save_path_all_txt="L:\\word_docs\\NLP\\",
    future_option=False):
    """
    Appends as string all texts in to one .txt file and print the 10 most common tokens. 
    """

    #initialise
    all_txt_stem = ""


    for txt_file in os.listdir(path_to_folder):
        path_to_doc = os.path.join(path_to_folder, txt_file)

        #open the file
        pt_txt = open_txt_file(path_to_doc)
        all_txt_stem = all_txt_stem + " " + pt_txt

        # save all_txt
    
    save_filtered_txt_file("made_up\\all_txt_stemmed2.txt", all_txt_stem, save_path_all_txt)
    
    # in order to count, use tokens   
    counts = count_tokens(all_txt_stem)
    


