from pathlib import Path
import random


BASE_DIR = Path(__file__).resolve().parents[2]
DICT_DIR = BASE_DIR / "dict"

FOUR_LETTER_WORDS_FILE = DICT_DIR / "palavras_4.txt"
FIVE_LETTER_WORDS_FILE = DICT_DIR / "palavras_5.txt"
SIX_LETTER_WORDS_FILE = DICT_DIR / "palavras_6.txt"
SEVEN_LETTER_WORDS_FILE = DICT_DIR / "palavras_7.txt"
EIGHT_LETTER_WORDS_FILE = DICT_DIR / "palavras_8.txt"

class WordService:
    def get_word(self, length: int, theme: str = None):
        match length:
            case 4:
                return self._get_random_word(FOUR_LETTER_WORDS_FILE)
            case 5:
                return self._get_random_word(FIVE_LETTER_WORDS_FILE)
            case 6:
                return self._get_random_word(SIX_LETTER_WORDS_FILE)
            case 7:
                return self._get_random_word(SEVEN_LETTER_WORDS_FILE)
            case 8:
                return self._get_random_word(EIGHT_LETTER_WORDS_FILE)
            case _:
                raise ValueError("Length must be between 4 and 8.")
    
    def _get_random_word(self, file_path: Path):
        if not file_path.exists():
            raise FileNotFoundError(f"Word file '{file_path}' not found.")
        
        with file_path.open('r', encoding='utf-8') as f:
            words = [line.strip() for line in f if line.strip()]
        
        if not words:
            raise ValueError(f"No words found in '{file_path}'.")
        
        return random.choice(words)
