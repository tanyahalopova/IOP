import os
from collections import defaultdict

LEMMAS_FOLDER = ("../task_2/lemmas")
INDEX_FILE = "inverted_index.txt"
index = defaultdict(set)

for filename in os.listdir(LEMMAS_FOLDER):
    filepath = os.path.join(LEMMAS_FOLDER, filename)
    doc_name = filename.replace("_lemmas.txt", "")
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            if not parts:
                continue
            lemma = parts[0]
            index[lemma].add(doc_name)

# сохраняем индекс
with open(INDEX_FILE, "w", encoding="utf-8") as f:
    for lemma in sorted(index):
        docs = " ".join(sorted(index[lemma]))
        f.write(f"{lemma}: {docs}\n")
print("Инвертированный индекс построен")