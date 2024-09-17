# translate_words.py: Integrates with the translation API, handles translation, 
# and manages API interactions.

#import deepl
from deep_translator import GoogleTranslator

def translate_words(database, sourceLang):
    # Add English words column.
    def addEnglishColumn(sqlConnection):    
        sqlCursor = sqlConnection.cursor()
        sqlCursor.execute("ALTER TABLE originalWords ADD COLUMN english TEXT")
        sqlConnection.commit()

    addEnglishColumn(database)

    #auth_key = "e9e3ce70-8257-4b23-83bd-d18047a89cab:fx"
    sqlCursor = database.cursor()
    sqlCursor.execute("SELECT word FROM originalWords WHERE english IS NULL")
    words = sqlCursor.fetchall()
    
    translator = GoogleTranslator(source=sourceLang, target='en')

    untranslatedWords = []
    i = 0
    batch_size = 250

    while i < len(words):
        percentage = (i/len(words))*100
        print(str(percentage) + "%")
        
        if i+batch_size<len(words):
            batch = [word_tuple[0] for word_tuple in words[i:i + batch_size]]
            i+=batch_size
        else:
            batch = [word_tuple[0] for word_tuple in words[i:len(words)]]
            i = len(words)

        try:
            translations = translator.translate_batch(batch)
        except Exception as e:
            print(f"Translation error for batch {batch}: {e}")
            untranslatedWords.extend(batch)
            continue

        # Iterate through the batch and the returned translations
        for untranslated_word, english_word in zip(batch, translations):
            if english_word and english_word != untranslated_word:
                # Update the database with the translation
                sqlCursor.execute("UPDATE originalWords SET english = ? WHERE word = ?", (english_word, untranslated_word))
            else:
                untranslatedWords.append(untranslated_word)
                sqlCursor.execute("DELETE FROM originalWords WHERE word = ?", (untranslated_word,))
            
            
    database.commit()
    return database

    #sqlCursor.execute("SELECT * FROM originalWords ORDER BY frequency ASC")
    #for row in sqlCursor.fetchall():
    #    print(row)

    