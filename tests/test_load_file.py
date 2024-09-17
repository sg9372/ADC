import unittest
from unittest.mock import MagicMock, patch
from src.load_file import getRawText

class TestLoadFile(unittest.TestCase):

    def test_getRawTextTest(self):
        pdfPath = "./data/raw/load_file_test_data.pdf"
        expected_output = "This is the test DATA! \n[]=#@ \n"
        result = getRawText(pdfPath)
        self.assertEqual(result, expected_output)