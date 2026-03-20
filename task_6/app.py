import os
import re
import math
from flask import Flask, render_template, request
import pymorphy3
from collections import Counter

app = Flask(__name__)

TFIDF_FOLDER = "../task_4/tfidf_lemmas"
INDEX_FILE = "../task_3/inverted_index.txt"

morph = pymorphy3.MorphAnalyzer()

#  загрузка TF-IDF
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


# загрузка индекса
index = {}
all_docs = set()

with open(INDEX_FILE, encoding="utf-8") as f:
    for line in f:
        lemma, docs = line.strip().split(":")
        docs_set = set(docs.strip().split())

        index[lemma] = docs_set
        all_docs.update(docs_set)


#  функции
def normalize(word):
    return morph.parse(word)[0].normal_form


def boolean_search(query):
    tokens = re.findall(r'\w+|AND|OR|NOT|\(|\)', query)
    stack = []

    for token in tokens:
        t = token.lower()
        if t in ["and", "и"]:
            b = stack.pop()
            a = stack.pop()
            stack.append(a & b)
        elif t in ["or", "или"]:
            b = stack.pop()
            a = stack.pop()
            stack.append(a | b)
        elif t in ["not", "не"]:
            a = stack.pop()
            stack.append(all_docs - a)
        elif token == "(":
            stack.append("(")
        elif token == ")":
            pass
        else:
            lemma = normalize(t)
            stack.append(index.get(lemma, set()))
    return stack[-1] if stack else set()


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


def cosine(v1, v2):
    dot = sum(v1.get(k, 0) * v2.get(k, 0) for k in v1)

    norm1 = math.sqrt(sum(v**2 for v in v1.values()))
    norm2 = math.sqrt(sum(v**2 for v in v2.values()))

    if norm1 == 0 or norm2 == 0:
        return 0

    return dot / (norm1 * norm2)


def search(query):

    filtered_docs = boolean_search(query)

    q_vector = build_query_vector(query)

    results = []

    for doc in filtered_docs:
        d_vector = documents.get(doc, {})
        score = cosine(q_vector, d_vector)

        if score > 0:
            results.append((doc, score))

    results.sort(key=lambda x: x[1], reverse=True)

    return results[:10]


# ---------- WEB ----------
@app.route("/", methods=["GET", "POST"])
def index_page():
    results = []

    if request.method == "POST":
        query = request.form["query"]
        results = search(query)

    return render_template("index.html", results=results)


if __name__ == "__main__":
    app.run(debug=True)