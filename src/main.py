from load_book import getRawText
from extract_words import extract_words
from translate_words import translate_words
#from generate_cue_cards import generate_cue_cards

def main(pdf_path):
    print("Starting the process...")

    # Load the book
    print("Loading the book...")
    text = getRawText(pdf_path)
    
    if text:
        # Extract words
        print("Extracting words...")
        wordsDatabase = extract_words(text)
        
        # Translate words
        print("Translating words...")
        translations = translate_words(wordsDatabase, sourceLang)
##        
##        # Generate cue cards
##        print("Generating cue cards...")
##        generate_cue_cards(translations)
##        
##        print("Process completed successfully!")
##    else:
##        print("Failed to load the book.")
##
##if __name__ == "__main__":
##    import sys
##    if len(sys.argv) != 2:
##        print("Usage: python main.py <path_to_pdf>")
##        sys.exit(1)
##    
##    pdf_path = sys.argv[1]
pdf_path = "./data/raw/test_data.pdf"
sourceLang = "ES"
main(pdf_path)