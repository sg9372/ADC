# process_words.py: Processes raw text from "load_book.py" into 

from nltk.tokenize import word_tokenize
import spacy
import re
    
def extract_words(raw_text):
    text = raw_text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    lemmatize(text)

    

def lemmatize(text):
    nlp = spacy.load("es_core_news_sm")
    doc = nlp(text)
    lemmas = [token.lemma_ for token in doc]
    print(lemmas)

#def sql_storage(tokenised_text):
