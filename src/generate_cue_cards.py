# generate_cue_cards.py: Uses the Anki-connect API to create and manage Anki cards.

import genanki

def generate_cue_cards(database, deck_name, output_file):
    sqlCursor = database.cursor()
    
    deck = genanki.Deck(deck_id=1234567890, name=deck_name)
    sqlCursor.execute("SELECT word, english FROM originalWords ORDER BY frequency DESC")
    rows = sqlCursor.fetchall()
    nMostCommon = 1

    for row in rows:
        spanish_word = row[0]
        english_word = row[1]

        # Create a card for each word and its translation
        note = genanki.Note(
            model=genanki.BASIC_MODEL,
            fields=[spanish_word + '<br><br>' + str(nMostCommon),english_word]
        )

        # Add the card to the deck
        deck.add_note(note)

        nMostCommon +=1


    # Save the deck to a file
    output_file = "./data/processed/" + output_file
    genanki.Package(deck).write_to_file(output_file)

    # Close the database connection
    database.close()