# Book Translator & Anki Card Generator

This project processes a Spanish PDF (later to add other foreign languages), extracts and lemmatizes verbs, translates them into English, and creates Anki flashcards for language learning. The program works at a rate of approx. 10 seconds per page.

## Features
- Reads foreign language PDF.
- Extracts verbs and calculates their frequency.
- Translates words using Google Translator.
- Generates Anki cue cards automatically.

## Requirements
- Python 3.8+
- See `requirements.txt` for a full list of dependencies.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/your-repo.git
    cd your-repo

2. Set up a virtual environment and install dependencies:
    python3 -m venv venv
    source venv/bin/activate  # On Windows: `venv\Scripts\activate`
    pip install -r requirements.txt

3. Store desired pdf in "raw" folder. 

4. To process a book and create Anki cards, run in termainl, for example:
    python src/main.py "./data/raw/Harry-Potter-III.pdf" "es" "test_deck"

5. On the Anki desktop App, select "import..." and navigate to 'your-repo/data/processed'

## Future Work

- Add additional langauge processing ability.
- Improve run time (currently this is largly due  the translation API).

