import os
import json
import random


chapter_mode = True
setname = 'test_other'
use_chapter = '_chapter'
minlen = 1000
maxlen = 1000
context = '_1000'

info_json = 'bookinfo{}_{}{}.json'.format(use_chapter, setname, context)
book_ID_mapping = {}
with open('speaker_book.txt') as fin:
    for line in fin:
        elems = line.split('|')
        ID = elems[0].lstrip().strip()
        speaker = elems[1].lstrip().strip()
        subset = elems[3].lstrip().strip()
        book = elems[5].lstrip().strip()
        if (speaker, book) not in book_ID_mapping:
            book_ID_mapping[(speaker, book)] = [ID]
        else:
            book_ID_mapping[(speaker, book)].append(ID)

with open(info_json) as fin:
    spk_bookwords = json.load(fin)

worddict = set()
with open('../all_rare_words.txt') as fin:
    for line in fin:
        word = line.strip()
        worddict.add(word)

worddict_full = {}
with open('word_freq.txt') as fin:
    for line in fin:
        word, freq = line.split()
        worddict_full[word] = int(freq)

spk_book_KB = {}

KBfulllist = set()

for speaker, books in spk_bookwords.items():
    # spk_book_KB[speaker] = {}
    for book, content in books.items():
        speaker_book_IDs =  book_ID_mapping[(speaker, book)] if 'chapter' not in info_json else [speaker]
        for speaker_book_ID in speaker_book_IDs:
            spk_book_KB[speaker_book_ID] = []
            bookwords = content['bookwords']
            oovwords = content['oovwords']
            for word in bookwords:
                if word in worddict:
                    spk_book_KB[speaker_book_ID].append((word, worddict_full[word] if word in worddict_full else 0)) 
                    if word not in KBfulllist:
                        KBfulllist.add(word)
            for word in oovwords:
                if word in worddict:
                    spk_book_KB[speaker_book_ID].append((word, worddict_full[word] if word in worddict_full else 0))
                    if word not in KBfulllist:
                        KBfulllist.add(word)

full_wordlist = list(KBfulllist)
output_path = 'LibriKB{}{}all_{}'.format(use_chapter[1:], context, maxlen)
os.system('mkdir -p {}'.format(output_path))
worddict = list(worddict)
for ID, KB in spk_book_KB.items():
    random.shuffle(worddict)
    count = 0
    while len(KB) < minlen and count < len(worddict):
        word = worddict[count]
        freq = worddict_full[word] if word in worddict_full else 0
        if (word, freq) not in KB:
            KB.append((word, freq))
        count += 1
    KB.sort(key=lambda tup: tup[1])
    with open(os.path.join(output_path, ID), 'w') as fout:
        for word, freq in KB[:maxlen]:
            fout.write(word+'\n')
