# translate_words.py: Integrates with the translation API, handles translation, 
# and manages API interactions.

import deepl

def translate_words(database, sourceLang):
    # Add English words column.
    def addEnglishColumn(sqlConnection):    
        sqlCursor = sqlConnection.cursor()
        sqlCursor.execute("ALTER TABLE spanishWords ADD COLUMN english TEXT")
        sqlConnection.commit()

    addEnglishColumn(database)

    auth_key = "e9e3ce70-8257-4b23-83bd-d18047a89cab:fx"
    translator = deepl.Translator(auth_key)

    sqlCursor = database.cursor()
    sqlCursor.execute("SELECT word FROM spanishWords WHERE english IS NULL")
    words = sqlCursor.fetchall()
    untranslatedWords = []
    i = 0
    batch_size = 50

    while i < len(words):
        if i+50<len(words):
            batch = [word_tuple[0] for word_tuple in words[i:i + batch_size]]
            i+=50
        else:
            batch = [word_tuple[0] for word_tuple in words[i:len(words)]]
            i = len(words)

        try:
            # Send the batch of words to DeepL for translation
            translations = translator.translate_text(batch, source_lang="ES", target_lang="EN-GB")

            # Iterate through the batch and the returned translations
            for untranslated_word, english_word in zip(batch, translations):
                if english_word.text and english_word.text != untranslated_word:
                    # Update the database with the translation
                    sqlCursor.execute("UPDATE spanishWords SET english = ? WHERE word = ?", (english_word.text, untranslated_word))
                else:
                    untranslatedWords.append(untranslated_word)
                    sqlCursor.execute("DELETE FROM spanishWords WHERE word = ?", (untranslated_word,))
        except deepl.DeepLException as e:
            print(f"Error with translation: {e}")
            untranslatedWords.extend(batch)

    database.commit()

    sqlCursor.execute("SELECT * FROM spanishWords ORDER BY frequency ASC")
    for row in sqlCursor.fetchall():
        print(row)

    print(untranslatedWords)

    database.close()