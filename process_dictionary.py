from pathlib import Path

INPUT_FILE="Lista-de-Palavras.txt"
OUTPUT_DIR="output_palavras"

def process_dictionary(input_path: str, output_dir: str):
    input_path = Path(input_path)
    output_dir = Path(output_dir)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file '{input_path}' not found.")
    
    output_dir.mkdir(parents=True, exist_ok=True)

    buckets = {length: [] for length in range(4, 9)}
    
    with input_path.open('r', encoding='utf-8') as file:
        for line in file:
            word = line.strip()

            if not (4 <= len(word) <= 8):
                continue

            if "-" in word:
                continue

            buckets[len(word)].append(word)

    for length, words in buckets.items():
        output_file = output_dir / f"palavras_{length}.txt"
        with output_file.open('w', encoding='utf-8') as f:
            for word in words:
                f.write(word + '\n')
                
if __name__ == "__main__":
    process_dictionary(INPUT_FILE, OUTPUT_DIR)
    print("=== END ===")