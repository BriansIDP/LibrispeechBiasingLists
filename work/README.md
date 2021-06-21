## Extracting chapter and book-level biasing lists

### Dependencies
* [spaCy](https://spacy.io/) is adopted for text normalisation.
* You should have text files for books downloaded together with [Librispeech](https://www.openslr.org/12)

### Files
* `get_book_chapters.py`: The script to scrape a specific range of text
* `booklist`: Paths to books
* `speaker_book.txt`: Speaker-book mappings
* `word_freq.txt`: Frequency of words appeared in the 960-hour training data
* `select_words.py`: Arrange biasing lists from all scraped words

### How To
* Run `python get_book_chapters.py` with correct set name in the script to get a json file containing word lists for each speaker-project pair.
* Run `select_words.py` 
