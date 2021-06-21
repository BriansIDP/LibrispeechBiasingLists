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
* First run: ```python get_book_chapters.py```. Need to set correct set name and range of text in the script. This outputs a json file containing biasing lists for each speaker-project pair.
* Then run: ```python select_words.py```. This takes the biasing lists and check it against `all_rare_words.txt`. Need to specify the set name, context length, the minimum and maximum length of each biasing list.
