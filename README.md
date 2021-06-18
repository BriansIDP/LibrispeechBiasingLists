# Librispeech Contextual Biasing Lists Arrangements

## Description
This repository contains biasing lists scraped at different levels. For utterance level, any word appeared in an utterance that belongs to `all_rare_words.txt` taken from [here](https://github.com/facebookresearch/fbai-speech/tree/master/is21_deep_bias). Chapter and book level biasing lists can be found in `ChapterLevel/` and `BookLevel/`. Each biasing list is indexed by the unique chapter ID assigned to it. The chapter ID is the first column in `chapter_location/test_clean_chapters` and `chapter_location/test_other_chapters`, and will be given in the utterance name during inference following the [ESPNet](https://github.com/espnet/espnet) recipe.

## Contents
* Full biasing list: `all_rare_words.txt`
* Chapter-level biasing lists: `ChapterLevel/`
* Book-level biasing lists: `BookLevel/`
* Location of chapters for each utterance: `chapter_location/`
* Procedure to generator biasing lists: `work/`
