import os
import math
from collections import Counter, defaultdict

TOKENS_FOLDER = "../task_2/tokens"
LEMMAS_FOLDER = "../task_2/lemmas"

OUT_TOKENS = "tfidf_tokens"
OUT_LEMMAS = "tfidf_lemmas"

os.makedirs(OUT_TOKENS, exist_ok=True)
os.makedirs(OUT_LEMMAS, exist_ok=True)


# Читаем токены 
docs_tokens = {}
df_tokens = defaultdict(int)
for filename in os.listdir(TOKENS_FOLDER):
    path = os.path.join(TOKENS_FOLDER, filename)
    doc = filename.replace("_tokens.txt", "")
    with open(path, encoding="utf-8") as f:
        tokens = [line.strip() for line in f if line.strip()]
    docs_tokens[doc] = tokens
    for term in set(tokens):
        df_tokens[term] += 1


# Читаем леммы 
docs_lemmas = {}
df_lemmas = defaultdict(int)
for filename in os.listdir(LEMMAS_FOLDER):
    path = os.path.join(LEMMAS_FOLDER, filename)
    doc = filename.replace("_lemmas.txt", "")
    lemmas = {}
    total_terms = 0
    with open(path, encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            if not parts:
                continue
            lemma = parts[0]
            forms = parts[1:]
            count = len(forms)
            lemmas[lemma] = count
            total_terms += count
    docs_lemmas[doc] = (lemmas, total_terms)
    for lemma in lemmas:
        df_lemmas[lemma] += 1


# IDF
N = len(docs_tokens)
idf_tokens = {
    term: math.log(N / df_tokens[term])
    for term in df_tokens
}
idf_lemmas = {
    lemma: math.log(N / df_lemmas[lemma])
    for lemma in df_lemmas
}


# 4. TF-IDF для токенов 
for doc, tokens in docs_tokens.items():
    total = len(tokens)
    tf = Counter(tokens)
    out_path = os.path.join(OUT_TOKENS, f"{doc}.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        for term in sorted(tf):
            tf_value = tf[term] / total
            tfidf = tf_value * idf_tokens[term]
            f.write(f"{term} {idf_tokens[term]:.6f} {tfidf:.6f}\n")


#  TF-IDF для лемм
for doc, (lemmas, total_terms) in docs_lemmas.items():
    out_path = os.path.join(OUT_LEMMAS, f"{doc}.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        for lemma in sorted(lemmas):
            tf_value = lemmas[lemma] / total_terms
            tfidf = tf_value * idf_lemmas[lemma]
            f.write(f"{lemma} {idf_lemmas[lemma]:.6f} {tfidf:.6f}\n")


print("TF-IDF посчитан")