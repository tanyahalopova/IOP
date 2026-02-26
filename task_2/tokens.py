import os
import re
from collections import defaultdict
import nltk
from nltk.corpus import stopwords
import pymorphy3

# При первом запуске:
# nltk.download('stopwords')

morph = pymorphy3.MorphAnalyzer()
stop_words = set(stopwords.words('russian'))

INPUT_FOLDER = "downloaded_pages"
TOKENS_FILE = "tokens.txt"
LEMMAS_FILE = "lemmas.txt"


def clean_and_tokenize(text):
    text = text.lower()
    text = re.sub(r'[^а-яё\s]', ' ', text)

    tokens = text.split()

    clean_tokens = []
    for token in tokens:
        if len(token) < 2:
            continue

        if token in stop_words:
            continue

        if token.isdigit():
            continue

        clean_tokens.append(token)

    return clean_tokens


def main():
    all_tokens = set()

    for filename in os.listdir(INPUT_FOLDER):
        filepath = os.path.join(INPUT_FOLDER, filename)

        if os.path.isfile(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
                tokens = clean_and_tokenize(text)
                all_tokens.update(tokens)

    #  Сохраняем список токенов
    with open(TOKENS_FILE, 'w', encoding='utf-8') as f:
        for token in sorted(all_tokens):
            f.write(token + "\n")

    # Группировка по леммам
    lemma_dict = defaultdict(list)

    for token in all_tokens:
        lemma = morph.parse(token)[0].normal_form
        lemma_dict[lemma].append(token)

    # Сохраняем леммы
    with open(LEMMAS_FILE, 'w', encoding='utf-8') as f:
        for lemma in sorted(lemma_dict.keys()):
            tokens_line = " ".join(sorted(lemma_dict[lemma]))
            f.write(f"{lemma} {tokens_line}\n")


if __name__ == "__main__":
    main()