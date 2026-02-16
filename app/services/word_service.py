from pathlib import Path
import json
import random


REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIRS = {
    "en-us": REPO_ROOT / "app" / "data" / "en-us",
    "pt-br": REPO_ROOT / "app" / "data" / "pt-br",
}
SUPPORTED_LANGS = {"en-us", "pt-br"}
DEFAULT_LANG = "en-us"
LENGTH_FILENAME_EN = {
    4: "four.json",
    5: "five.json",
    6: "six.json",
    7: "seven.json",
    8: "eight.json",
}
LENGTH_DIR_PT = {
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
}
_WORDNET_CACHE: dict[tuple[str, int], dict[str, dict[str, list[str]]]] = {}
_PT_BR_LETTER_CACHE: dict[tuple[int, str], dict[str, dict[str, list[str]]]] = {}


class WordService:
    def get_word(self, length: int, lang: str = DEFAULT_LANG):
        lang = _normalize_lang(lang)
        if lang == "pt-br":
            if length < 3 or length > 8:
                raise ValueError("Length must be between 3 and 8 for pt-br.")
        else:
            if length < 4 or length > 8:
                raise ValueError("Length must be between 4 and 8.")

        bucket = _load_wordnet_length(lang, length)
        if not bucket:
            raise ValueError(f"No words found for length {length}.")

        word = random.choice(list(bucket))
        entry = bucket[word]
        return _normalize_entry(word, entry, lang)
    
    def get_meanings(self, word: str, lang: str = DEFAULT_LANG) -> dict[str, list[str]]:
        lang = _normalize_lang(lang)
        word = word.strip().lower()
        if not word:
            raise ValueError("Word must not be empty.")

        word_len = len(word)
        if lang == "pt-br":
            if word_len in LENGTH_DIR_PT:
                bucket = _load_pt_br_letter(word_len, word[0])
                if word in bucket:
                    return _normalize_entry(word, bucket[word], lang)

            for length in LENGTH_DIR_PT:
                bucket = _load_pt_br_letter(length, word[0])
                if word in bucket:
                    return _normalize_entry(word, bucket[word], lang)
            raise ValueError(f"Word '{word}' not found in wordnet.")

        if word_len in LENGTH_FILENAME_EN:
            bucket = _load_wordnet_length(lang, word_len)
            if word in bucket:
                return _normalize_entry(word, bucket[word], lang)

        for length in LENGTH_FILENAME_EN:
            bucket = _load_wordnet_length(lang, length)
            if word in bucket:
                return _normalize_entry(word, bucket[word], lang)
        raise ValueError(f"Word '{word}' not found in wordnet.")

def _normalize_lang(lang: str) -> str:
    if not lang:
        return DEFAULT_LANG
    lang = lang.strip().lower()
    if lang not in SUPPORTED_LANGS:
        raise ValueError(f"Unsupported lang '{lang}'. Use one of: en-us, pt-br.")
    return lang

def _normalize_entry(word: str, entry: dict[str, list[str]], lang: str) -> dict[str, list[str]]:
    if not isinstance(entry, dict):
        raise ValueError("Invalid wordnet entry format.")

    definitions = entry.get("definitions", [])
    synonyms = entry.get("synonyms", [])
    if lang == "pt-br":
        usages = entry.get("usages", entry.get("examples", []))
    else:
        usages = entry.get("usages", [])

    return {
        "word": word,
        "definitions": definitions,
        "synonyms": synonyms,
        "usages": usages,
    }

def _load_wordnet_length(lang: str, length: int) -> dict[str, dict[str, list[str]]]:
    if lang == "en-us":
        return _load_en_us_length(length)
    if lang == "pt-br":
        return _load_pt_br_length(length)
    raise ValueError(f"Unsupported lang '{lang}'. Use one of: en-us, pt-br.")

def _load_en_us_length(length: int) -> dict[str, dict[str, list[str]]]:
    if length not in LENGTH_FILENAME_EN:
        raise ValueError("Length must be between 4 and 8.")

    cache_key = ("en-us", length)
    cached = _WORDNET_CACHE.get(cache_key)
    if cached is not None:
        return cached

    path = DATA_DIRS["en-us"] / LENGTH_FILENAME_EN[length]
    if not path.exists():
        raise FileNotFoundError(f"Word file '{path}' not found.")

    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict):
        raise ValueError("Invalid wordnet JSON format.")

    _WORDNET_CACHE[cache_key] = data
    return data

def _load_pt_br_length(length: int) -> dict[str, dict[str, list[str]]]:
    if length not in LENGTH_DIR_PT:
        raise ValueError("Length must be between 3 and 8 for pt-br.")

    cache_key = ("pt-br", length)
    cached = _WORDNET_CACHE.get(cache_key)
    if cached is not None:
        return cached

    length_dir = DATA_DIRS["pt-br"] / LENGTH_DIR_PT[length]
    if not length_dir.exists():
        raise FileNotFoundError(f"Word directory '{length_dir}' not found.")

    merged: dict[str, dict[str, list[str]]] = {}
    for path in length_dir.glob("*.json"):
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            raise ValueError(f"Invalid wordnet JSON format in '{path}'.")
        merged.update(data)

    _WORDNET_CACHE[cache_key] = merged
    return merged

def _load_pt_br_letter(length: int, letter: str) -> dict[str, dict[str, list[str]]]:
    if length not in LENGTH_DIR_PT:
        return {}

    letter = (letter or "").strip().lower()
    if not letter:
        return {}

    cache_key = (length, letter)
    cached = _PT_BR_LETTER_CACHE.get(cache_key)
    if cached is not None:
        return cached

    length_dir = DATA_DIRS["pt-br"] / LENGTH_DIR_PT[length]
    path = length_dir / f"{letter}.json"
    if not path.exists():
        _PT_BR_LETTER_CACHE[cache_key] = {}
        return {}

    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError(f"Invalid wordnet JSON format in '{path}'.")

    _PT_BR_LETTER_CACHE[cache_key] = data
    return data
