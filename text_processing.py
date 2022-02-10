from typing import Dict, List, Optional, Tuple
from itertools import groupby
import random
import nltk
nltk.download('stopwords')

from nltk.tokenize.treebank import TreebankWordDetokenizer
from nltk.corpus import stopwords

STOPWORDS = set(stopwords.words('english'))

def is_in_stopwords(word):
    return word in STOPWORDS

def sentence_contains_word(sentence: str, word: str) -> bool:
    return word.lower() in nltk.wordpunct_tokenize(sentence.lower())

def select_bio_sentence_using_word(bio_sentences: Dict[str, str], word: str) -> Tuple[str, str]:
    sentence_candidates: Dict[str, str] = {
        name: sentence for name, sentence in bio_sentences.items()
        if sentence_contains_word(sentence, word)
    }
    if len(sentence_candidates) == 0:
        raise Exception("No sentences contain word")
    final_name = random.choice(list(sentence_candidates.keys()))
    return sentence_candidates[final_name], final_name

def deplicate_sequential_words(tokens: List[str], word_list: List[str]) -> List[str]:
    previous = None
    final_tokens = []
    for token in tokens:
        if previous != token or not (token in word_list):
            final_tokens.append(token)
        previous = token
    return final_tokens

s = 'Since Gordon loved fantasy, he was watching Avatar when his mother came in and shot him.'
name = "Gordon Ramsey"

def transform_sentence_to_second_person(sentence: str, name: str = ""):
    pronouns = {
        "she": "you",
        "her": "your",
        "he": "you",
        "him": "you",
        "his": "your",
    }
    verbs = {
        "was": "were",
        "is": "are"
    }
    names = {name_part: "you" for name_part in name.split()}

    tokens: List[str] = nltk.wordpunct_tokenize(sentence)
    # Fix name parts
    tokens = [names.get(word, word) for word in tokens]
    tokens = deplicate_sequential_words(tokens, ["you"])
    # Fix pronouns
    tokens = [pronouns.get(word.lower(), word) for word in tokens]
    # Fix verbs
    tokens = [
        verbs.get(word, word) if index > 0 and tokens[index - 1] == "you" else word
        for index, word in enumerate(tokens)
    ]

    return TreebankWordDetokenizer().detokenize(tokens).capitalize()

print(transform_sentence_to_second_person(s, name))
