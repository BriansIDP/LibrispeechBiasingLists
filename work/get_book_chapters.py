import sys, os
import json
import en_core_web_md

nlp = en_core_web_md.load()
context = 1000

latin_books = ['/scratch/gs534/librispeech/LibriSpeech/books/ascii/3178/3178.txt',
               '/scratch/gs534/librispeech/LibriSpeech/books/ascii/4770/wasoe10.txt',
               '/scratch/gs534/librispeech/LibriSpeech/books/ascii/19019/19019.txt',
               '/scratch/gs534/librispeech/LibriSpeech/books/ascii/3440/61001108.txt',
               '/scratch/gs534/librispeech/LibriSpeech/books/ascii/3436/21001107.txt',
               '/scratch/gs534/librispeech/LibriSpeech/books/ascii/3441/71001107.txt']

def normalise_text(line):
    doc = nlp(line.strip())
    text = [w.text.upper() for w in doc]
    merged_text = []
    for i, word in enumerate(text):
        if i > 0 and word == '\'S':
            merged_text[-1] = merged_text[-1] + '\'S'
        else:
            merged_text.append(word)
    #     if w.tag_ in ['NNPS', 'NNP']:
    #         text.append(w.text.upper())
    return merged_text

def get_context(lines, start, end, context, full_len):
    if full_len > context and context > (end - start):
        halflen = (context - (end - start)) // 2
        if start < halflen:
            start = 0
            end = context
        elif full_len - end < halflen:
            start = full_len - context
            end = full_len
        else:
            start = start - halflen
            end = end + halflen
    elif full_len < context:
        start = 0
        end = full_len
    return lines[start: end]

spk_info = {}
setname = 'test-other'

with open('CHAPTERS/test_other_chapters') as fin:
    for line in fin:
        elems = line.split('|')
        proj_ID = elems[0].lstrip().strip()
        speaker = elems[1].lstrip().strip()
        subset = elems[3].lstrip().strip()
        book = elems[5].lstrip().strip()
        chapter_s = int(elems[6].lstrip().strip())
        chapter_e = int(elems[7].lstrip().strip())
        if proj_ID not in spk_info:
            spk_info[proj_ID] = []
        spk_info[proj_ID].append([subset, book, chapter_s, chapter_e])

books = {}
with open('booklist') as fin:
    for book in fin:
        bookid = book.strip().split('/')[-1]
        books[bookid] = book.strip()

vocab = {}
with open('word_freq.txt') as fin:
    for line in fin:
        word, freq = line.split()
        vocab[word] = freq

bookinfo = {}
for proj_ID, infos in spk_info.items():
    for info in infos:
        if info[0] == setname:
            bookwords = set()
            oovwords = set()
            encoding = 'utf-8' if 'utf-8' in books[info[1]] else 'ascii'
            for bookfile in os.listdir(books[info[1]]):
                if bookfile.endswith('.txt') or '.txt' in bookfile:
                    bookpath = os.path.join(books[info[1]], bookfile)
                    print(bookpath)
                    if bookpath in latin_books:
                        encoding = 'latin-1'
                    start, end = info[2], info[3]
                    with open(bookpath, encoding=encoding) as fin:
                        lines = fin.readlines()
                        if context == 0:
                            lines = lines[start:end]
                        else:
                            lines = get_context(lines, start, end, context, len(lines))
                    for line in lines:
                        words = normalise_text(line)
                        for word in words:
                            if word not in bookwords and word in vocab:
                                bookwords.add(word)
                            elif word not in bookwords and word not in oovwords and word not in vocab:
                                oovwords.add(word)
            if proj_ID not in bookinfo:
                bookinfo[proj_ID] = {}
            bookinfo[proj_ID][info[1]] = {'bookwords':list(bookwords), 'oovwords':list(oovwords)}
            # print(bookpath)
with open('bookinfo_chapter_test_other_{}.json'.format(context), 'w') as fout:
    json.dump(bookinfo, fout, indent=4)

