from pathlib import Path
import json
import random


BASE_DIR = Path(__file__).resolve().parents[2]
DICT_DIR = BASE_DIR / "dict"
WORDNET_JSON_FILE = DICT_DIR / "wordnet_words_len4_8.json"
_WORDNET_CACHE: dict[str, dict[str, list[str]]] | None = None


class WordService:
    def get_word(self, length: int, theme: str = None):
        if length < 4 or length > 8:
            raise ValueError("Length must be between 4 and 8.")

        data = _load_wordnet()
        bucket_key = _bucket_key_for_length(length)
        bucket = data.get(bucket_key)
        if not bucket:
            raise ValueError(f"No words found for length {length}.")

        return random.choice(list(bucket))
    
    def get_meanings(self, word: str) -> list[str]:
        word = word.strip().lower()
        data = _load_wordnet()

        for bucket in data.values():
            if word in bucket:
                meanings = bucket[word]
                return meanings
        raise ValueError(f"Word '{word}' not found in wordnet.")

def _bucket_key_for_length(length: int) -> str:
    match length:
        case 4:
            return "len_four"
        case 5:
            return "len_five"
        case 6:
            return "len_six"
        case 7:
            return "len_seven"
        case 8:
            return "len_eight"
        case _:
            raise ValueError("Length must be between 4 and 8.")


def _load_wordnet() -> dict[str, dict[str, list[str]]]:
    global _WORDNET_CACHE
    if _WORDNET_CACHE is not None:
        return _WORDNET_CACHE

    if not WORDNET_JSON_FILE.exists():
        raise FileNotFoundError(f"Word file '{WORDNET_JSON_FILE}' not found.")

    with WORDNET_JSON_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict):
        raise ValueError("Invalid wordnet JSON format.")

    _WORDNET_CACHE = data
    return data
