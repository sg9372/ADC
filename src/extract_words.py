# process_words.py: Processes raw text from "load_book.py" into 

import spacy
import re
import sqlite3
    
def extract_words(raw_text):
    text = raw_text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return lemmatize(text)

def lemmatize(text):
    nlp = spacy.load("es_core_news_sm")
    doc = nlp(text)
    lemmas = [token.lemma_ for token in doc if token.pos_ != ('PROPN') and token.is_alpha]
    return sql_storage(lemmas)

def sql_storage(lemmas_list):
    sqlConnection = sqlite3.connect("originalWords.db")
    sqlCursor = sqlConnection.cursor()

    sqlCursor.execute("DROP TABLE IF EXISTS originalWords")
    sqlCursor.execute("CREATE TABLE IF NOT EXISTS originalWords(word TEXT PRIMARY KEY, frequency INTEGER)")
    # ~584 words per page

    word_count = {}
    
    # Collect words and frequencies in memory
    for lemma in lemmas_list:
        if lemma in word_count:
            word_count[lemma] += 1
        else:
            word_count[lemma] = 1
    
    for word, frequency in word_count.items():
        sqlCursor.execute("INSERT INTO originalWords(word, frequency) VALUES(?, ?) "
                          "ON CONFLICT(word) DO UPDATE SET frequency = frequency + ?",
                          (word, frequency, frequency))
    
    sqlCursor.execute("SELECT COUNT(*) FROM originalWords")
    result = sqlCursor.fetchone()
    print(str(result[0]))
    
    return sqlConnection