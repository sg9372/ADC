import unittest
from unittest.mock import patch, MagicMock
import sqlite3
from src.translate_words import addEnglishColumn, translate_and_add_words, translate_words

class TestTranslateWords(unittest.TestCase):

    def setUp(self):
        # Set up an in-memory SQLite database for testing
        self.connection = sqlite3.connect(':memory:')
        self.connection.execute("CREATE TABLE originalWords(word TEXT PRIMARY KEY, frequency INTEGER)")
        self.connection.execute("INSERT INTO originalWords (word, frequency) VALUES ('hola', 1)")
        self.connection.execute("INSERT INTO originalWords (word, frequency) VALUES ('mundo', 1)")
        self.connection.commit()

    def tearDown(self):
        self.connection.close()

    def test_addEnglishColumn(self):
        # Test adding the English column
        addEnglishColumn(self.connection)
        cursor = self.connection.execute("PRAGMA table_info(originalWords)")
        columns = [info[1] for info in cursor.fetchall()]
        self.assertIn('english', columns)

    @patch('src.translate_words.GoogleTranslator.translate_batch')
    def test_translate_and_add_words(self, mock_translate_batch):
        # Mock translation
        mock_translate_batch.return_value = ['hello', 'world']
        
        # Test translating and adding words to the DB
        translate_and_add_words(self.connection, sourceLang='es')

        cursor = self.connection.execute("SELECT word, english FROM originalWords")
        results = cursor.fetchall()
        expected = [('hola', 'hello'), ('mundo', 'world')]
        self.assertEqual(results, expected)

    @patch('src.translate_words.GoogleTranslator.translate_batch')
    def test_translate_words(self, mock_translate_batch):
        # Mock translation
        mock_translate_batch.return_value = ['hello']

        # Test the high-level translate_words function
        translate_words(self.connection, sourceLang='es')

        cursor = self.connection.execute("SELECT word, english FROM originalWords WHERE word = 'hola'")
        result = cursor.fetchone()
        print(result)
        self.assertEqual(result, ('hola', 'hello'))

if __name__ == '__main__':
    unittest.main()
