import os
from collections import defaultdict

TOKENS_FOLDER = "../task_2/tokens"
INDEX_FILE = "inverted_index.txt"

index = defaultdict(set)

# читаем все файлы токенов
for filename in os.listdir(TOKENS_FOLDER):
    filepath = os.path.join(TOKENS_FOLDER, filename)
    doc_name = filename.replace("_tokens.txt", "")
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            token = line.strip()
            index[token].add(doc_name)

# сохраняем индекс
with open(INDEX_FILE, "w", encoding="utf-8") as f:
    for token in sorted(index):
        docs = " ".join(sorted(index[token]))
        f.write(f"{token}: {docs}\n")

print("Индекс создан")