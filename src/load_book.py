# load_book.py: Handles loading and reading the book content.

import pymupdf

def getRawText(file_path: str):
    doc = pymupdf.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text 
