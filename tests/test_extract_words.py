import unittest
import sqlite3
from unittest.mock import MagicMock, patch
from src.extract_words import tokenize, lemmatize, sql_storage

class TestExtractWords(unittest.TestCase):

    def test_tokenize(self):
        raw_text = "Hola todos, este es mi atempto a verificar."
        expected_output = "hola todos este es mi atempto a verificar"
        result = tokenize(raw_text)
        self.assertEqual(result, expected_output)

    @patch('spacy.load')
    def test_lemmatize(self, mock_spacy_load):
        mock_nlp = MagicMock()
        mock_doc = [
            MagicMock(lemma_='ser', pos_='VERB', is_alpha=True),
            MagicMock(lemma_='hola', pos_='INTJ', is_alpha=True),
            MagicMock(lemma_='Juan', pos_='PROPN', is_alpha=True),  # Proper noun (excluded)
        ]
        mock_nlp.return_value = mock_doc
        mock_spacy_load.return_value = mock_nlp

        result = lemmatize("Hola Juan")
        self.assertEqual(result, ['ser', 'hola'])

    def test_sql_storage(self):
        lemmas = ['hola', 'mundo', 'hola']

        # Create an in-memory SQLite DB for testing (so we don't modify the actual database)
        connection = sqlite3.connect(':memory:')

        # Mock the connection behavior to use our in-memory DB
        connection.execute("CREATE TABLE IF NOT EXISTS originalWords(word TEXT PRIMARY KEY, frequency INTEGER)")

        # Run the function
        connection = sql_storage(lemmas)

        cursor = connection.execute("SELECT word, frequency FROM originalWords WHERE word = 'hola'")
        result = cursor.fetchone()
        self.assertEqual(result, ('hola', 2))

