from typing import Dict, List, Optional
from text_processing import select_bio_sentence_using_word, transform_sentence_to_second_person, is_in_stopwords
from scraper_util import parse_bio_from_url, URL
from generate_bio_map import get_bio_urls_for_today
from generate_bio_map import generate_bio_map

BioDict = Dict[str, List[str]]

example_bios: BioDict = {
    "Lana Depop": [
        "Lana Depop was born in Isreal in 2021.",
        "Her parents were butchers.",
        "She had three brothers and one sister."
    ],
    "Beyonce Knowles": [
        "Beyonce was born Beyonce Knowles in 1843.",
        "Her parents were singers.",
        "She developed a love for rice rolls as a child.",
        "Soon thereafter, she had a tragic accident involving two miniature moose, from which she never fully recovered."
    ],
}

def get_next_sentence(bios: BioDict, sentence_index: int, input_word: str) -> Optional[str]:
    sentences_at_index: Dict[str, str] = {name: sentences[sentence_index] for name, sentences in bios.items() if sentence_index < len(sentences)}
    try:
        sentence, name = select_bio_sentence_using_word(sentences_at_index, input_word)
        return transform_sentence_to_second_person(sentence, name)
    except Exception as e:
        return None

def get_max_sentence_count(bios: BioDict) -> int:
    return max([len(sentences) for sentences in bios.values()])

def main():
    bios: BioDict = example_bios

    # name, sentences = parse_bio_from_url(URL)
    # if we have a file for today's date, parse and use that
    # TODO
    # else
    bios = generate_bio_map(get_bio_urls_for_today())
    # TODO: upload bios to file to store for subsequent runs

    print("A STORY OF YOU:")
    print("Instructions: At each >>, please enter a word and press ENTER.")
    print("---------------")

    words_entered: List[str] = ["born"]
    max_sentence_count: int = get_max_sentence_count(bios)

    for sentence_index in range(max_sentence_count):
        next_sentence: str = get_next_sentence(bios, sentence_index, words_entered[-1])
        if (next_sentence is None):
            break
        else:
            print(f"\"{next_sentence}\"")
            input_word: str = input(">> ")
            if (len(input_word) < 1):
                print(f"(your word \"{input_word}\" must be at least 1 letter long.)")
                break
            if (is_in_stopwords(input_word)):
                print(f"(your word \"{input_word}\" must not be a common stopword.)")
                break
            words_entered.append(input_word)


    print("\"Then you died.\"")
    print(".")
    print(".")
    print(".")
    print("---------------")

if __name__ == "__main__":
    main()
