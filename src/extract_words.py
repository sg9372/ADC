# process_words.py: Processes raw text from "load_book.py" into 

from nltk.tokenize import word_tokenize

import re

#def sql_storage(tokenised_text):
    


def extract_words(raw_text):
    text = raw_text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    tokenised_text = word_tokenize(text)
    ss = SnowballStemmer('spanish')
    for i in range(len(tokenised_text)):
        tokenised_text[i] = ss.stem(tokenised_text[i])
    print(tokenised_text)
