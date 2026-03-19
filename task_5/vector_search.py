import os
import re
import math
import pymorphy3
from collections import Counter

TFIDF_FOLDER = "../task_4/tfidf_lemmas"
INDEX_FILE = "../task_3/inverted_index.txt"

morph = pymorphy3.MorphAnalyzer()

# загрузка TF-IDF 
documents = {}
idf = {}

for filename in os.listdir(TFIDF_FOLDER):
    path = os.path.join(TFIDF_FOLDER, filename)
    doc_name = filename.replace(".txt", "")
    vector = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            lemma, idf_val, tfidf_val = line.strip().split()
            vector[lemma] = float(tfidf_val)
            idf[lemma] = float(idf_val)
    documents[doc_name] = vector


#  загрузка индекса 
index = {}
all_docs = set()

with open(INDEX_FILE, encoding="utf-8") as f:
    for line in f:
        lemma, docs = line.strip().split(":")
        docs_set = set(docs.strip().split())
        index[lemma] = docs_set
        all_docs.update(docs_set)


# лемматизация
def normalize(word):
    return morph.parse(word)[0].normal_form


#  boolean поиск 
def boolean_search(query):
    tokens = re.findall(r'\w+|AND|OR|NOT|\(|\)', query)
    expr = []
    for token in tokens:
        t = token.lower()
        if t == "and":
            expr.append("&")
        elif t == "or":
            expr.append("|")
        elif t == "not":
            expr.append("all_docs -")
        elif token in ["(", ")"]:
            expr.append(token)
        else:
            lemma = normalize(t)
            docs = index.get(lemma, set())
            expr.append(str(docs))
    return eval(" ".join(expr))


#  вектор запроса 
def build_query_vector(query):
    words = re.findall(r'\w+', query.lower())
    lemmas = [normalize(w) for w in words]
    tf = Counter(lemmas)
    total = len(lemmas)
    vector = {}
    for lemma in tf:
        if lemma not in idf:
            continue
        tf_val = tf[lemma] / total
        vector[lemma] = tf_val * idf[lemma]
    return vector


# cosine 
def cosine(v1, v2):
    dot = sum(v1.get(k, 0) * v2.get(k, 0) for k in v1)
    norm1 = math.sqrt(sum(v**2 for v in v1.values()))
    norm2 = math.sqrt(sum(v**2 for v in v2.values()))
    if norm1 == 0 or norm2 == 0:
        return 0
    return dot / (norm1 * norm2)


#  гибридный поиск 
def search(query):
    # 1. фильтрация через boolean
    filtered_docs = boolean_search(query)
    # 2. вектор запроса
    q_vector = build_query_vector(query)
    results = []
    for doc in filtered_docs:
        d_vector = documents.get(doc, {})
        score = cosine(q_vector, d_vector)
        results.append((doc, score))
    results.sort(key=lambda x: x[1], reverse=True)
    return results


#  запуск
while True:
    query = input("Введите запрос: ")
    results = search(query)
    print("\nРезультаты:")
    if not results:
        print("Ничего не найдено")
        continue
    for doc, score in results:
        print(f"{doc}: {score:.4f}")