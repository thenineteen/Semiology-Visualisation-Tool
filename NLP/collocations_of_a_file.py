import nltk



def collocations_of_a_file(file="L:\\word_docs\\NLP\\filtered_tokenised\\test\\all_txt_stem.txt"):
    
    with open(file) as f:
        txtstring = f.read()

    txtstring_tokens = nltk.word_tokenize(txtstring)  # list of tokens

    txtstring_tokens_nltk = nltk.Text(txtstring_tokens) # nltk.text.Text tyep

    return txtstring_tokens_nltk.collocations()