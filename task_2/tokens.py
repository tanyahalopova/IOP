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

INPUT_FOLDER = "../task_1/downloaded_pages"
TOKENS_FOLDER = "tokens"
LEMMAS_FOLDER = "lemmas"

os.makedirs(TOKENS_FOLDER, exist_ok=True)
os.makedirs(LEMMAS_FOLDER, exist_ok=True)


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

    return list(set(clean_tokens))

for filename in os.listdir(INPUT_FOLDER):

    filepath = os.path.join(INPUT_FOLDER, filename)

    if not os.path.isfile(filepath):
        continue

    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    tokens = clean_and_tokenize(text)
    name = os.path.splitext(filename)[0]

    #  TOKENS
    tokens_file = os.path.join(TOKENS_FOLDER, f"{name}_tokens.txt")

    with open(tokens_file, "w", encoding="utf-8") as f:
        for token in sorted(tokens):
            f.write(token + "\n")

    # LEMMAS
    lemma_dict = defaultdict(list)

    for token in tokens:
        lemma = morph.parse(token)[0].normal_form
        lemma_dict[lemma].append(token)

    lemmas_file = os.path.join(LEMMAS_FOLDER, f"{name}_lemmas.txt")

    with open(lemmas_file, "w", encoding="utf-8") as f:
        for lemma in sorted(lemma_dict):
            token_line = " ".join(sorted(lemma_dict[lemma]))
            f.write(f"{lemma} {token_line}\n")