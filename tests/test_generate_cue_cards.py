import unittest
from unittest.mock import MagicMock, patch
import sqlite3
from src.generate_cue_cards import generate_cue_cards

class TestGenerateCueCards(unittest.TestCase):

    def setUp(self):
        # Set up an in-memory SQLite database for testing
        self.connection = sqlite3.connect(':memory:')
        self.connection.execute("CREATE TABLE originalWords(word TEXT PRIMARY KEY, english TEXT, frequency INTEGER)")
        self.connection.execute("INSERT INTO originalWords (word, english, frequency) VALUES ('hola', 'hello', 10)")
        self.connection.execute("INSERT INTO originalWords (word, english, frequency) VALUES ('mundo', 'world', 5)")
        self.connection.execute("INSERT INTO originalWords (word, english, frequency) VALUES ('adios', 'goodbye', 2)")
        self.connection.commit()

    def tearDown(self):
        # Close the connection after the test
        self.connection.close()

    @patch('src.generate_cue_cards.genanki.Deck')
    @patch('src.generate_cue_cards.genanki.Note')
    @patch('src.generate_cue_cards.genanki.Package')
    def test_generate_cue_cards(self, mock_package, mock_note, mock_deck):
        # Mock the creation of deck and note objects
        mock_deck_instance = MagicMock()
        mock_deck.return_value = mock_deck_instance
        
        mock_note_instance = MagicMock()
        mock_note.return_value = mock_note_instance

        # Run the function
        generate_cue_cards(self.connection, deck_name='Test Deck', output_file='output.apkg')

        # Check that a deck was created with the correct name
        mock_deck.assert_called_once_with(deck_id=1234567890, name='Test Deck')

        # Ensure that notes were created for each word in the table and added to the deck
        expected_calls = [
            (('hola<br><br>1', 'hello'),),
            (('mundo<br><br>2', 'world'),),
            (('adios<br><br>3', 'goodbye'),)
        ]
        self.assertEqual(mock_note.call_count, 3)

        # Check that notes were added to the deck
        self.assertEqual(mock_deck_instance.add_note.call_count, 3)

        # Check that the output file was written
        mock_package.assert_called_once_with(mock_deck_instance)
        mock_package_instance = mock_package.return_value
        mock_package_instance.write_to_file.assert_called_once_with('./data/processed/output.apkg')

if __name__ == '__main__':
    unittest.main()
